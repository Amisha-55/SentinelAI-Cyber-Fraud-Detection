# Gemini explainer module

import google.generativeai as genai

import os

from dotenv import load_dotenv


load_dotenv()


genai.configure(

api_key=os.getenv("GOOGLE_API_KEY")

)



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

