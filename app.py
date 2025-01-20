# app.py
from flask import Flask, request, jsonify
from conveyor_belt import ConveyorBelt
from llm_controller import LLMController
import simpy
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize simulation
env = simpy.Environment()
belt = ConveyorBelt(env)

# Initialize LLM with more detailed logging
try:
    llm = LLMController()
    logger.info("LLM Controller initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize LLM Controller: {e}")
    raise

@app.route("/command", methods=["POST"])
def process_command():
    try:
        data = request.json
        if not data or "command" not in data:
            return jsonify({"status": "error", "message": "No command provided"}), 400

        command = data["command"]
        logger.info(f"Received command: {command}")

        # Parse command using LLM
        llm_response = llm.parse_command(command)
        logger.info(f"LLM parsed response: {llm_response}")

        # Initialize response
        response = {"status": "error", "message": "Unknown command"}
        
        # Process the parsed command
        if llm_response.startswith("Error"):
            response = {"status": "error", "message": llm_response}
        elif llm_response == "START":
            response = {"status": "success", "message": belt.start()}
        elif llm_response == "STOP":
            response = {"status": "success", "message": belt.stop()}
        elif llm_response.startswith("ADJUST_SPEED"):
            try:
                speed = float(llm_response.split()[1])
                response = {"status": "success", "message": belt.adjust_speed(speed)}
            except (IndexError, ValueError) as e:
                response = {"status": "error", "message": f"Invalid speed value: {str(e)}"}
        
        logger.info(f"Final response: {response}")
        return jsonify(response)

    except Exception as e:
        logger.error(f"Error processing command: {str(e)}")
        return jsonify({"status": "error", "message": f"Internal server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)