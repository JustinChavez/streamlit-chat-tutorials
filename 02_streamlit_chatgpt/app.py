# Libraries
import streamlit as st
from streamlit_chat import message
import openai
from decouple import config
import tempfile
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
import os

# Setup OpenAI
openai.organization = config("OPENAI_ORG_ID")
openai.api_key = config("OPENAI_API_KEY")

INDEX = config("INDEX")

# Initialise streamlit session state variables
st.session_state.setdefault('messages', [
    {"role": "system", "content": "Your name is StreamlitGPT"}
])
st.session_state.setdefault('ai_message', [])
st.session_state.setdefault('user_message', [])
url_params = st.experimental_get_query_params() 

if 'pdf_index' in url_params:
    st.session_state['pdf_index'] = url_params['pdf_index'][0]

# Setting page title and header
st.set_page_config(page_title="ChatWith")
st.markdown(f"<h1 style='text-align: center;'>StreamlitGPT</h1>", unsafe_allow_html=True)

# Function for interacting with ChatGPT API
def generate_response(prompt):
    vectorstore = FAISS.load_local(os.path.join(INDEX, st.session_state['pdf_index']), OpenAIEmbeddings(openai_api_key=config("OPENAI_API_KEY")))
    get_relevant_sources = vectorstore.similarity_search(prompt, k=2)

    template = f"\n\nUse the information below to help answer the user's question.\n\n{get_relevant_sources[0].page_content}\n\n{get_relevant_sources[1].page_content}"

    with st.expander("Source 1", expanded=False):
        st.write(get_relevant_sources[0].page_content)
    with st.expander("Source 2", expanded=False):
        st.write(get_relevant_sources[1].page_content)

    system_source_help = {"role": "system", "content": template}

    st.session_state['messages'].append({"role": "user", "content": prompt})

    # Get Previous messages and append context
    to_send = st.session_state['messages'].copy()
    to_send.insert(-1, system_source_help)

    st.session_state['messages'].append({"role": "user", "content": prompt})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=to_send,
    )
    response = completion.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": response})

    return response

if "pdf_index" not in st.session_state:
    file_path = st.file_uploader(label="Upload a PDF file that your chatbot will use", type=['pdf'])

    if st.button("Index PDF", disabled=not bool(file_path)):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=True) as tmp_file:
            tmp_file.write(file_path.read())
            # LangChain PyPDF loader
            loader = PyPDFLoader(tmp_file.name)
            pages = loader.load_and_split()

            # Split the pages into chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
            page_chunks = text_splitter.split_documents(pages)

            # Embed into FAISS
            vectorstore = FAISS.from_documents(page_chunks, OpenAIEmbeddings(openai_api_key=config("OPENAI_API_KEY")))

            pdf_index = os.path.splitext(os.path.basename(file_path.name))[0]
            local_path = os.path.join(INDEX, pdf_index)

            vectorstore.save_local(local_path)

            # Save the file name to session state as pdf_index
            st.session_state['pdf_index'] = pdf_index

            # Direct user to the link to chat
            st.markdown(f"PDF indexed successfully as **{st.session_state.pdf_index}**. The app to chat with your document can be found here: [http://localhost:8501?pdf_index={st.session_state.pdf_index}](http://localhost:8501?pdf_index={st.session_state.pdf_index}).")
else:
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