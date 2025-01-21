AI-Agent for Intelligent Task Automation
This AI-Agent is a Streamlit-based application that provides three main functionalities:

Chatbot Support: Answer FAQs using Pinecone for vector search.

Weather & News Agent: Fetch real-time weather and news updates.

Personalized To-Do List Manager: Manage tasks with add, remove, and view functionalities.

Table of Contents:

Installation

Configuration

Running the Application

Project Structure

API Keys

FAQ Data

Troubleshooting

Contributing


Installation:

Prerequisites
Python 3.8 or higher

Git (optional, for cloning the repository)

Steps
Clone the repository:

git clone https://github.com/hamipirzada/AI-Agent.git
cd AI-Agent
Create a virtual environment:

python -m venv venv
Activate the virtual environment:

On Windows:

venv\Scripts\activate
On macOS/Linux:

source venv/bin/activate
Install dependencies:

pip install -r requirements.txt
Configuration
1. API Keys
The secrets.toml file is located in the .streamlit folder. Add the following API keys to .streamlit/secrets.toml:

toml
Copy
PINECONE_API_KEY = "your-pinecone-api-key"
PINECONE_ENVIRONMENT = "your-pinecone-environment"
OPENWEATHER_API_KEY = "your-openweather-api-key"
NEWS_API_KEY = "your-newsapi-key"
2. FAQ Data
Add your FAQ data to a faqs.json file in the root directory. The file should follow this format:

[
    {
        "question": "What is your return policy?",
        "answer": "We accept returns within 30 days."
    },
    {
        "question": "How do I track my order?",
        "answer": "Use our order tracking portal."
    }
]
Running the Application
Activate your virtual environment (if not already activated):

source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
Run the Streamlit app:

streamlit run Agent.py
Open your browser and navigate to:


http://localhost:8501
Project Structure

AI-Agent/
│
├── .gitignore
├── Agent.py                # Main application script
├── faqs.json               # FAQ data in JSON format
├── requirements.txt        # Python dependencies
├── README.md               # This guide
└── .streamlit/
    └── secrets.toml        # API keys and sensitive data
API Keys
You will need the following API keys:

Pinecone: For vector search functionality.

Sign up at Pinecone.

OpenWeather: For weather data.

Sign up at OpenWeather.

NewsAPI: For news headlines.

Sign up at NewsAPI.

FAQ Data
The faqs.json file contains the questions and answers for the chatbot. Add your own FAQs in the following format:

[
    {
        "question": "Your question here",
        "answer": "Your answer here"
    }
]
Troubleshooting
1. API Key Errors
Ensure the .streamlit/secrets.toml file is correctly formatted.

Verify that the API keys are valid and have the required permissions.

2. FAQ Data Not Loading
Check the faqs.json file for proper JSON formatting.

Ensure the file is in the root directory.

3. Streamlit Issues
Make sure Streamlit is installed:

pip install streamlit
If the app doesn't launch, check for errors in the terminal.

