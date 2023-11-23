from dotenv import load_dotenv
import os
import openai

# Load the .env file
load_dotenv()

print('here')
api_key = os.getenv('MY_VARIABLE')
print(api_key)