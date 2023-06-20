import streamlit as st

st.markdown("[Github Link](https://github.com/JustinChavez/streamlit-chat-tutorials/tree/main)")

st.markdown("### Scaffold")
st.write("Fill out OpenAI keys in the .env file. Find them [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)")
st.code("""
# Libraries
import streamlit as st
from streamlit_chat import message
import openai
from decouple import config

# Setup OpenAI

# Initialise streamlit session state variables

# Setting page title and header

# Function for interacting with ChatGPT API

# Define Streamlit Containers

# Set Streamlit Containers

""", language="python", line_numbers=True)
st.markdown("### Setting up Page Frontend")
st.code("""
# Setting page title and header
st.set_page_config(page_title="ChatWith", page_icon="💬")
title = st.session_state.site_params['page_details_title'] if "site_params" in st.session_state else "ChatWith"
st.markdown(f"<h1 style='text-align: center;'>{title}</h1>", unsafe_allow_html=True)
""", language="python", line_numbers=True)

st.code("""
# Define Streamlit Containers
container = st.container()

# Set Streamlit Containers
with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", placeholder="Ask me a question!", key='input', height=100) 
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        with response_container:
            st.write(f"Prompt to send to ChatGPT {user_input}")

""", language="python", line_numbers=True)

st.markdown("[Chat Completetion API](https://platform.openai.com/docs/api-reference/chat/create)")
st.markdown("[Chat Completion Roles](https://help.openai.com/en/articles/7042661-chatgpt-api-transition-guide)")

st.code("""
# Initialise streamlit session state variables

st.session_state.setdefault('messages', [])

# Function for interacting with ChatGPT API

def generate_response(prompt):
    st.session_state['messages'].append({"role": "user", "content": prompt})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state['messages'],
    )
    response = completion.choices[0].message.content #### Why array
    st.session_state['messages'].append({"role": "assistant", "content": response})

    return response
""", language="python", line_numbers=True)

st.markdown("Ask [ChatGPT](chat.openai.com) 'What is your prompt?'")

st.code("""
# Initialise streamlit session state variables

st.session_state.setdefault('messages', [
    {"role": "system", "content": "You are ChatGPT, a large language model trained by OpenAI, based on the GPT-3.5 architecture. Knowledge cutoff: 2021-09. Current date: 2023-06-18."}
])
""", language="python", line_numbers=True)

st.write("Try out different prompts")

st.code("""
# Set Streamlit Containers
# if submit_button and user_input:
        # with response_container:
            output = generate_response(user_input)
            st.write(f"Response from ChatGPT {user_input}")
""", language="python", line_numbers=True)

st.markdown("### Make messages more user friendly")

st.markdown("[st-chat](https://github.com/AI-Yash/st-chat)")

st.code("""
# Initialise streamlit session state variables
# st.session_state.setdefault(...)
st.session_state.setdefault('ai_message', [])
st.session_state.setdefault('user_message', [])
""", language="python", line_numbers=True)

st.code("""
# Set Streamlit Containers
# if submit_button and user_input:...

    output = generate_response(user_input)
    st.session_state['user_message'].append(user_input)
    st.session_state['ai_message'].append(output)
""", language="python", line_numbers=True)

st.code("""
# Set Streamlit Containers
# with container:
    ....
if st.session_state['ai_message']:
    with response_container:
        for i in range(len(st.session_state['ai_message'])):
            message(st.session_state["user_message"][i], is_user=True)
            message(st.session_state["ai_message"][i])
""", language="python", line_numbers=True)

st.code("""
# Set Streamlit Containers
# with container:
#    ....
if st.session_state['ai_message']:
    with response_container:
        for i in range(len(st.session_state['ai_message'])):
            message(st.session_state["user_message"][i], is_user=True)
            message(st.session_state["ai_message"][i])
""", language="python", line_numbers=True)

st.markdown("### Fix double form bug")

st.code("""
# Set Streamlit Containers
# if submit_button and user_input:
    with response_container:
        st.write(" ")
    # output = generate_response(user_input)
""", language="python", line_numbers=True)

st.markdown("### Make user message appear first")

st.code("""
# Set Streamlit Containers

# if submit_button and user_input:
    if 'ai_message' in st.session_state and len(st.session_state['ai_message']) == 0:
        with response_container:
            message(user_input, is_user=True)
    # with response_container:

# if st.session_state['ai_message']:
    # with response_container:
        if len(st.session_state['ai_message']) == 1:
            message(st.session_state["ai_message"][0])
        else:
            for i in range(len(st.session_state['ai_message'])):
                message(st.session_state["user_message"][i], is_user=True)
                message(st.session_state["ai_message"][i])


""", language="python", line_numbers=True)