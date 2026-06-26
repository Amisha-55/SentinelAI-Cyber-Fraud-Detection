# Gemini explainer module

from turtle import st

import google.generativeai as genai

import os

from dotenv import load_dotenv


load_dotenv()

# First, try to get the key from .env
api_key = os.getenv("GOOGLE_API_KEY")

# If not found, get it from Streamlit Secrets
if not api_key:

    api_key = st.secrets["GOOGLE_API_KEY"]

# Configure Gemini

genai.configure(api_key=api_key)

def get_gemini_response(text):


    model=genai.GenerativeModel(

        "gemini-1.5-flash"

    )


    prompt=f"""

You are an expert Cyber Security AI Assistant.


Analyze the following message:


{text}


Return in this format:


Scam Type :


Why it is dangerous:


Suspicious Keywords:


Risk Level:


Safety Tips:


"""


    response=model.generate_content(prompt)


    return response.text

