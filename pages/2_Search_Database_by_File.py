import streamlit as st
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
import utils

st.set_page_config(
    page_title="Chat with database",
    page_icon="👋",
)

st.write("# Search Database by File")

uploaded_file = st.file_uploader("Upload a Case File", accept_multiple_files=False, type=['pdf'])

if uploaded_file:
    st.write(uploaded_file.name)
    utils.empty_directory('prompt_data')
    utils.save_uploaded_file('prompt_data', uploaded_file)
    

st.sidebar.success("Select a demo above.")

st.markdown(
    """

"""
)