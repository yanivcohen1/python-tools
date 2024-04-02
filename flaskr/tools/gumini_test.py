# https://ai.google.dev/tutorials/python_quickstart
import pathlib
import textwrap
import os
from dotenv import load_dotenv
from pathlib import Path
import configparser

config = configparser.ConfigParser()
secsecss = config.read('flaskr/tools/env_local.ini')
GEMINI_API_KEY = config['DEFAULT']['GEMINI_API_KEY']
# dotenv_path = Path('yaniv/.env.local')
# load_dotenv(dotenv_path=dotenv_path)

# GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

import google.generativeai as genai

# from IPython.display import display
# from IPython.display import Markdown


# def to_markdown(text):
#     text = text.replace('•', '  *')
#     return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


# Used to securely store your API key
# from google.colab import userdata

# Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
# GOOGLE_API_KEY=userdata.get('GOOGLE_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)


for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)

model = genai.GenerativeModel('gemini-pro')
# response = model.generate_content("What is the meaning of life?")
# print(response.text)
# # print(response.candidates)

# print("test pass")
while True:
    query = input("enter query:")
    response = model.generate_content(query)
    print(response.text)
