# llm_controller.py
import requests
import time
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMController:
    def __init__(self, model_name="phi"):
        self.model_name = model_name
        self.base_url = "http://ollama:11434"
        self.max_retries = 5
        self.retry_delay = 10  # seconds
        self._wait_for_ollama()
        logger.info(f"Ollama {model_name} model is ready for interaction.")

    def _wait_for_ollama(self):
        """Wait for Ollama service to be ready and model to be loaded"""
        logger.info("Waiting for Ollama service to be ready...")
        
        for attempt in range(self.max_retries):
            try:
                response = requests.get(f"{self.base_url}/api/tags")
                if response.status_code == 200:
                    models = response.json().get("models", [])
                    available_models = [m.get("name", "") for m in models]
                    logger.info(f"Available models: {available_models}")
                    
                    if f"{self.model_name}:latest" in available_models:
                        # Test the model with a simple prompt
                        test_response = self._test_model()
                        if test_response:
                            logger.info(f"Model {self.model_name} is ready and responding!")
                            return True
                    else:
                        logger.info(f"Model {self.model_name} not found, attempting to pull...")
                        self._pull_model()
                
                logger.info(f"Attempt {attempt + 1}/{self.max_retries} - Waiting for {self.retry_delay} seconds...")
                time.sleep(self.retry_delay)
            except requests.exceptions.RequestException as e:
                logger.error(f"Connection error: {e}")
                time.sleep(self.retry_delay)
        
        raise Exception(f"Could not initialize Ollama service after {self.max_retries} attempts")

    def _test_model(self):
        """Test the model with a simple prompt"""
        try:
            test_prompt = """Task: Parse the following command for a conveyor belt system.
Command: test
Please respond with one of these actions: START, STOP, or ADJUST_SPEED with value.
Response:"""
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": f"{self.model_name}:latest",
                    "prompt": test_prompt,
                    "stream": False,
                    "temperature": 0.1,
                    "max_tokens": 50
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return bool(response.json().get("response", "").strip())
            return False
        except Exception as e:
            logger.error(f"Error testing model: {str(e)}")
            return False

    def _pull_model(self):
        """Pull the model if it's not available"""
        try:
            logger.info(f"Pulling model {self.model_name}...")
            response = requests.post(
                f"{self.base_url}/api/pull",
                json={"name": self.model_name},
                timeout=300
            )
            if response.status_code == 200:
                logger.info(f"Successfully pulled model {self.model_name}")
                return True
            else:
                logger.error(f"Failed to pull model: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error pulling model: {str(e)}")
            return False

    def parse_command(self, command):
        try:
            # Create a more structured prompt
            prompt = f"""Task: Parse the following command for a conveyor belt system.
Command: {command}
Please respond with one of these actions: START, STOP, or ADJUST_SPEED with value.
Response:"""

            logger.info(f"Sending prompt to model: {prompt}")
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": f"{self.model_name}:latest",
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.1,
                    "max_tokens": 50
                },
                timeout=30
            )

            if response.status_code == 200:
                response_data = response.json()
                action = response_data.get("response", "").strip()
                logger.info(f"Raw model response: {action}")
                
                if not action:
                    logger.error("Empty response from model")
                    return "Error: Empty response from model"
                
                # Process the response
                if "start" in action.lower():
                    return "START"
                elif "stop" in action.lower():
                    return "STOP"
                elif "speed" in action.lower():
                    try:
                        # Try to extract a number from the response
                        import re
                        numbers = re.findall(r'\d+', action)
                        if numbers:
                            return f"ADJUST_SPEED {numbers[0]}"
                    except:
                        pass
                
                return action
            else:
                error_msg = f"Error: {response.status_code} - {response.text}"
                logger.error(error_msg)
                return error_msg
                
        except requests.exceptions.Timeout:
            logger.error("Request timed out")
            return "Error: Request timed out"
        except requests.exceptions.ConnectionError:
            logger.error("Could not connect to Ollama service")
            return "Error: Could not connect to Ollama service"
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return f"Error: {str(e)}"