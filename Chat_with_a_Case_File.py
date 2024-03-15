import streamlit as st
import pandas as pd
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from IPython.display import Markdown, display
import chromadb
from ragger import ragger

st.set_page_config(
    page_title="Legal AI",
    page_icon="🤖",
)

ragger = ragger()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "show_chat_interface" not in st.session_state:
    st.session_state.show_chat_interface = False

if "chat_document_index" not in st.session_state:
    st.session_state.chat_document_index = 0

st.write("# Chat with a Case File")

df = pd.read_csv('metadata_doc4_gpt003s_0.csv')

df_no_duplicates = df.drop_duplicates(subset=['pdf_name'])

# Use a text_input to get the keywords to filter the dataframe
text_search = st.text_input("Search Casefiles", value="")

names_list = df_no_duplicates['legible_name'].tolist()

# Filter the list based on the search text
filtered_names = [name for name in names_list if text_search.lower() in name.lower()]

chat_buttons = []

if text_search:
    # Show the cards
    N_cards_per_row = 3
    if text_search:
        for n_row, row in enumerate(filtered_names):
            i = n_row%N_cards_per_row
            if i==0:
                st.write("---")
                cols = st.columns(N_cards_per_row, gap="large")
            # draw the card
            with cols[n_row%N_cards_per_row]:
                st.caption(f"{row}")
                chat_buttons.append(st.button("Chat", key=n_row))

for i, button in enumerate(chat_buttons):
    if button:
        # st.write(f"{filtered_names[i]}")
        st.session_state.chat_document_index = i
        st.session_state.show_chat_interface=True
        st.session_state.messages = []



if st.session_state.show_chat_interface:

    ragger.create_db_link()

    st.write("---")
    st.markdown(f"### Chatting with Case File -> :green[{filtered_names[st.session_state.chat_document_index]}]")
    # print(st.session_state.chat_document_index)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            query_pdf_name = df_no_duplicates.loc[df['legible_name'] == filtered_names[st.session_state.chat_document_index], 'pdf_name'].iloc[0]
            response = ragger.query_single_file_data(prompt, query_pdf_name)

            # response = 'test response'
            # response = st.write_stream(stream)
            st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        # print(st.session_state.messages)