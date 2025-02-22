# ConveyorGPT: Intelligent Conveyor Belt Control System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Overview

ConveyorGPT is an intelligent conveyor belt control system that leverages natural language processing to interpret and execute commands for industrial automation. It bridges the gap between human operators and machinery by allowing natural language control of conveyor belt operations.

### Key Benefits:
- Natural language control of industrial equipment
- Reduced training time for new operators
- Improved safety through standardized command interpretation
- Real-time speed adjustments and operation monitoring
- Detailed logging for operation tracking and debugging

## 🏗️ System Architecture

The system consists of three main components:

1. **Flask API Server (app.py)**
   - Handles HTTP requests for conveyor belt control
   - Manages error handling and response formatting
   - Integrates with LLM Controller and Conveyor Belt modules

2. **LLM Controller (llm_controller.py)**
   - Processes natural language commands
   - Converts human instructions into system commands
   - Provides standardized command interpretation

3. **Conveyor Belt Controller (conveyor_belt.py)**
   - Manages conveyor belt operations
   - Controls speed adjustments
   - Handles start/stop operations
   - Uses SimPy for simulation and timing control

## 🛠️ Technical Stack

- **Backend Framework**: Flask
- **Simulation Engine**: SimPy
- **Natural Language Processing**: Custom LLM Controller
- **Logging**: Python's built-in logging module
- **API Format**: JSON
- **Development Language**: Python 3.x

## 📋 Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/conveyor-gpt.git
cd conveyor-gpt
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

1. Create a `.env` file in the project root:
```
LLM_API_KEY=your_api_key_here
FLASK_ENV=development
LOG_LEVEL=INFO
```

2. Configure logging levels in `app.py` if needed:
```python
logging.basicConfig(level=logging.INFO)
```

## 🏃‍♂️ Running the Application

1. Start the Flask server:
```bash
python app.py
```

The server will start on `http://0.0.0.0:5000`

## 🔄 API Endpoints

### POST /command
Controls the conveyor belt through natural language commands.

**Request Body:**
```json
{
    "command": "start the conveyor belt"
}
```

**Successful Response:**
```json
{
    "status": "success",
    "message": "Conveyor belt started successfully"
}
```

**Error Response:**
```json
{
    "status": "error",
    "message": "Error description here"
}
```

## 📝 Supported Commands

- Start the conveyor belt
- Stop the conveyor belt
- Adjust speed to [value] meters per second
- Emergency stop
- Check current status

## 🔍 Monitoring and Logging

The application uses Python's logging module to track operations:
- Info level: Normal operations and command processing
- Error level: Failed operations and system errors
- Debug level: Detailed system information (when enabled)

Logs are output to standard output and can be redirected to a file if needed.

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

## 💻 Development

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## 📦 Project Structure

```
conveyor-gpt/
├── app.py                 # Main Flask application
├── conveyor_belt.py       # Conveyor belt control logic
├── llm_controller.py      # LLM integration and command parsing
├── tests/                 # Test suite
├── requirements.txt       # Project dependencies
├── .env                   # Environment variables
└── README.md             # Project documentation
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🏷️ Topics

- #IndustrialAutomation
- #NaturalLanguageProcessing
- #ConveyorControl
- #MachineLearning
- #IndustryAI
- #Python
- #Flask
- #Manufacturing
- #FactoryAutomation
- #IndustrialIoT
