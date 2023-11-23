import streamlit as st
from dotenv import load_dotenv
import os
import openai

# Load the .env file
load_dotenv()
with st.sidebar:
    openai.api_key =  os.getenv('MY_VARIABLE')
    #print(openai_api_key)
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"

st.title("🗺️ Dora Transport")
st.caption("Get from A to B")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    #st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("What is up"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0]["message"]["content"]
    st.text(msg)
    
    with st.chat_message("assistant"):
        st.markdown(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})


