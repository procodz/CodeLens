# Code Review Pipeline

This project provides a code review pipeline using a Flask backend and a React frontend. The pipeline includes various agents that analyze code for security, style, performance, and documentation issues.

## Features

- **Security Analysis**: Detects potential security vulnerabilities.
- **Style Analysis**: Ensures code follows best practices and style guidelines.
- **Performance Analysis**: Analyzes code for performance bottlenecks and optimization opportunities.
- **Documentation Analysis**: Checks for completeness and quality of documentation.

## Technologies Used

- **Backend**: Flask, Flask-CORS, Google Generative AI, Python
- **Frontend**: React, Axios
- **Environment Management**: Python-dotenv

## Installation

### Prerequisites

- Python 3.x
- Node.js and npm

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/code-review-pipeline.git
   cd code-review-pipeline
2. Create and activate a virtual environment:
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. Install the required Python packages:
    pip install -r requirements.txt
4. Create a .env file in the root directory and add your Google API key:
    GOOGLE_API_KEY=your_api_key_here
5. Run the Flask backend:
    python app.py

Frontend Setup:
    
1. Navigate to the code-review-ui directory:
    cd code-review-ui

2. Install the required npm packages:
    npm install

3. Start the React frontend:
    npm start

Usage
    Open your browser and go to http://localhost:3000.
    Paste your code into the text area.
    Click the "Review Code" button.
    View the review results displayed on the page.

Project Structure:

code-review-pipeline/
├── agents/
│   ├── agent_factory.py
│   ├── base_agent.py
│   ├── documentation_agent.py
│   ├── performance_agent.py
│   ├── security_agent.py
│   └── style_agent.py
├── code-review-ui/
│   ├── public/
│   │   ├── index.html
│   │   ├── manifest.json
│   │   └── robots.txt
│   ├── src/
│   │   ├── App.css
│   │   ├── App.js
│   │   ├── App.test.js
│   │   ├── index.css
│   │   ├── index.js
│   │   ├── logo.svg
│   │   ├── reportWebVitals.js
│   │   └── setupTests.js
│   ├── .gitignore
│   ├── package.json
│   └── README.md
├── utils/
│   ├── code_parser.py
│   ├── issue_tracker.py
│   └── result_formatter.py
├── .gitignore
├── app.py
├── main.py
├── README.md
└── requirements.txt

Contributing:
    Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.