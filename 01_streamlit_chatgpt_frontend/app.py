# Libraries
import streamlit as st
from streamlit_chat import message
import openai
from decouple import config

# Setup OpenAI
openai.organization = config("OPENAI_ORG_ID")
openai.api_key = config("OPENAI_API_KEY")

# Initialise streamlit session state variables
st.session_state.setdefault('messages', [
    {"role": "system", "content": "Your name is StreamlitGPT"}
])
st.session_state.setdefault('ai_message', [])
st.session_state.setdefault('user_message', [])

# Setting page title and header
st.set_page_config(page_title="ChatWith")
st.markdown(f"<h1 style='text-align: center;'>StreamlitGPT</h1>", unsafe_allow_html=True)

# Function for interacting with ChatGPT API
def generate_response(prompt):
    st.session_state['messages'].append({"role": "user", "content": prompt})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state['messages'],
    )
    response = completion.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": response})

    return response

# Define Streamlit Containers
response_container = st.container()
container = st.container()

# Set Streamlit Containers
with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", placeholder="Ask me a question!", key='input', height=100) 
        submit_button = st.form_submit_button(label='Send')

        if submit_button and user_input:
            if 'ai_message' in st.session_state and len(st.session_state['ai_message']) == 0:
                with response_container:
                    message(user_input, is_user=True)
            output = generate_response(user_input)
            st.session_state['user_message'].append(user_input)
            st.session_state['ai_message'].append(output)

if st.session_state['ai_message']:
    with response_container:
        if len(st.session_state['ai_message']) == 1:
            message(st.session_state["ai_message"][0])
        else:
            for i in range(len(st.session_state['ai_message'])):
                message(st.session_state["user_message"][i], is_user=True)
                message(st.session_state["ai_message"][i])