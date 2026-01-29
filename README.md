COSC 461 – AI Python Tutor

This project implements an interactive AI-powered Python tutor using the OpenAI API.
The tutor needs to:

Explain Python concepts

Debug code

Provide examples

Generate practice exercises

Give adaptive feedback

Track token usage and cost (required for COSC 461)

Optionally run inside a Streamlit GUI

This application demonstrates prompt engineering, tokenization, model interaction, and conversational tutoring design.

Features:

LLM-powered tutoring using GPT-5.1 (or any OpenAI model set in .env)

Intent detection (explain / debug / exercise / code feedback / general help)

Structured responses (Concept Explanation, Code Example, Exercises, etc.)

Conversation memory

determine Token usage + cost estimation

Streamlit web interface (optional but added)

Project Structure
cosc461-ai-tutor/
│
├── .env
├── main.py               # Command-line tutor
├── tutor.py              # needs to have Core logic, prompt templates, and intent detection
├── streamlit_app.py      # an optional GUI with Streamlit
├── requirements.txt
└── README.md

Setup Instructions
1. Install Python 3.10+

Download from https://www.python.org
 if needed.

2. Create a virtual environment (recommended)
python -m venv venv


Activate it:

Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt


Your requirements.txt should include:

openai>=1.0.0
python-dotenv
tiktoken
streamlit

4. Create a .env file

Inside the project directory, create:

OPENAI_API_KEY=your-api-key-here
MODEL=gpt-5.1

# Optional cost estimation fields (for gpt-5.1)
PRICE_PER_1K_PROMPT_TOKENS=0.00125  #pricing for gpt-5.1 tken
PRICE_PER_1K_COMPLETION_TOKENS=0.01

5. Run the Tutor (Command Line Interface)
python main.py


Example tests:

You: explain python loops
You: why does this code give an error?
You: give me a practice exercise on functions

6. Run the Tutor (Streamlit GUI)
streamlit run streamlit_app.py


The browser will open automatically at:

http://localhost:8501/

Quit Streamlit

Press:

CTRL + C