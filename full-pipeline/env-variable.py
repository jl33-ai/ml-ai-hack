from dotenv import load_dotenv
import os
import openai

# Load the .env file
load_dotenv()

openai.api_key =  os.getenv('MY_VARIABLE')

response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{'role': 'assistant', 'content': 'How can I help you?'}, {'role': 'user', 'content': 'Hi how are you'}])
msg = response.choices[0]["message"]["content"]
print(msg)