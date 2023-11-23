import streamlit as st, os, openai, features, json
from dotenv import load_dotenv

NUM_ITERS = 5

# Load the .env file
load_dotenv()
with st.sidebar:
    openai.api_key =  os.getenv('MY_VARIABLE')
    #print(openai_api_key)
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"

st.title("🗺️ Dora Transport")
st.caption("Get from A to B")
st.text('HGEh')



if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages, functions=features.DETAILS)
    st.text(response['choices'][0])
    finish_reason, i, message = response['choices'][0]

    # model wants to utilise a custom feature
    if (finish_reason == "function_call"):
        feature_responses = [response]

        for _i in range(NUM_ITERS):
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=feature_responses, functions=features.DETAILS)
            finish_reason, i, msg = response['choices'][0]

            match finish_reason:
                case 'function_call':
                    feature = features.OPTIONS.get(msg['function_call'])
                    arguments = list(json.loads(feature['arguments']).values())
                    print(arguments)
                    feature_response = feature(*arguments)
                    feature_responses.append({"role": "function", "name": feature['name'], "content": f"Result = {str(feature_response)}"})
                case 'stop':
                    feature_responses.append(msg)
                    break
    
        # feature-enriched answer is what the user wants
        message = feature_responses[-1]

    text = message['content']
    
    st.session_state.messages.append({"role": "assistant", "content": text})
    st.chat_message("assistant").write(text)
