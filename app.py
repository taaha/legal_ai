import streamlit as st
import os
import shutil
from ragger import ragger
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

ragger = ragger()


st.sidebar.header("File Uploader")
uploaded_files = st.sidebar.file_uploader("Upload Document", type=['pdf'], disabled=False, accept_multiple_files=True)

# st.divider()
if st.sidebar.button("Embed Documents"):
    st.sidebar.info("Embedding documents...")
    try:
        for uploaded_file in uploaded_files:
            with open(f"./documents/{uploaded_file.name}", mode='wb') as w:
                w.write(uploaded_file.getvalue())
        ragger.reingest()
        # embed_pdf.embed_all_pdf_docs()
        st.sidebar.info("Done!")
    except Exception as e:
        st.sidebar.error(e)
        st.sidebar.error("Failed to embed documents.")

ragger.create_db_link()

# create the app
st.title("Legal AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = ragger.query_data(prompt)
        # response = st.write_stream(stream)
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    # print(st.session_state.messages)