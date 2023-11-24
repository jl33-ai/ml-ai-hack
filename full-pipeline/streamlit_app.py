import streamlit as st, features
from openai import OpenAI
from io import StringIO
import json


NUM_ITERS = 3

client = OpenAI(api_key=st.secrets['ai_api'])
first_run = True


# Function to convert chat messages to a JSON string
def convert_chat_to_json(chat_history):
    return json.dumps(chat_history, indent=2)

'''
# In the sidebar or wherever you want the button
with st.sidebar:
    chat_history_json = convert_chat_to_json(st.session_state.messages)
    # Create a string buffer
    chat_history_buffer = StringIO(chat_history_json)
    # Create the download button
    st.download_button(
        label="Download Chat History",
        data=chat_history_buffer,
        file_name="chat_history.json",
        mime="application/json"
    )
'''

    # ADD THIS TO BOTTOM LEFT

with st.sidebar:
    "# Made by:"
    "🐧 Harrison"
    "🐬 Hannah"
    "🧚‍♀️ Jane"
    "👨‍🌾 Justin"
    "🐯 Will"
    "---"
    "For [ML AI HACK 2023](https://www.aihackmelb.com)"
    "Check out the [source](https://github.com/jl33-ai/ml-ai-hack)"




st.title("Dora Transport")
st.caption("🗺️🎒🚂 Let me guide you from A to B")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if (first_run):

        first_run = False

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    feature_responses = st.session_state.messages.copy()

    # check if model wants to utilise a custom feature
    for _i in range(NUM_ITERS):
        # api output
        response = client.chat.completions.create(model="gpt-4", messages=feature_responses, functions=features.DETAILS).choices[0]
        message = response.message
        finish_reason = response.finish_reason

        if finish_reason == "function_call":
            # model requests feature in form of json
            desired_feature = message.function_call
            # get the signature of the feature from constant array
            feature_function = features.OPTIONS.get(desired_feature.name)
            # arguments are located in the response json
            # args = list(json.loads(desired_feature.arguments).values())
            # perform: response = feature(arg1, arg2, arg3)
            feature_response = feature_function #(*args)

            # new message generated from feature output
            feature_responses.append({"role": "function", "name": desired_feature.name, "content": "Result = " + str(feature_response)})

            # features not needed to answer query/all relevant features utilised
        elif finish_reason == 'stop':
            # feature-enriched answer is what the user wants
            st.session_state.messages.append({"role": "assistant", "content": message.content})
            st.chat_message("assistant").write(message.content)
            break
