import streamlit as st, os, openai, features, json
from dotenv import load_dotenv

NUM_ITERS = 3

# Load the .env file
load_dotenv()
with st.sidebar:
    # ADD THIS TO BOTTOM LEFT 
    openai.api_key =  os.getenv('MY_VARIABLE')
    #print(openai_api_key)
    
    "# Made by "
    "🐬 Hannah" 
    "👨‍🌾 Justin"
    "🐠 Harrison"
    "🐯 Will (LLM master and Site Engineer)"
    "🐙 Jane"
    "for [ML AI HACK 2023](https://www.aihackmelb.com)"


st.title("Dora Transport")
st.caption("🗺️🎒🚂 Let me guide you from A to B")


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    feature_responses = st.session_state.messages.copy()

    # check if model wants to utilise a custom feature
    for _i in range(NUM_ITERS):
        # api output
        response = openai.ChatCompletion.create(model="gpt-4", messages=feature_responses, functions=features.DETAILS)['choices'][0]
        message = response['message']
        finish_reason = response['finish_reason']

        if finish_reason == "function_call":
            # model requests feature in form of json
            desired_feature = message['function_call']
            # get the signature of the feature from constant array
            feature_function = features.OPTIONS.get(desired_feature['name'])
            # arguments are located in the response json
            args = list(json.loads(desired_feature['arguments']).values())
            # perform: response = feature(arg1, arg2, arg3)
            feature_response = feature_function(*args)

            # new message generated from feature output
            feature_responses.append({"role": "function", "name": desired_feature['name'], "content": "Result = " + str(feature_response)})
        
            # features not needed to answer query/all relevant features utilised
        elif finish_reason == 'stop':
            # feature-enriched answer is what the user wants
            st.session_state.messages.append({"role": "assistant", "content": message['content']})
            st.chat_message("assistant").write(message['content'])
            break
