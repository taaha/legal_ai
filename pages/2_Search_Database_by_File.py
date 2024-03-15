import streamlit as st
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
import pandas as pd
import os
import utils
from ragger import ragger

st.set_page_config(
    page_title="Legal AI",
    page_icon="🤖",
)

ragger = ragger()

df = pd.read_csv('metadata_doc4_gpt003s_0_detailed.csv')

st.write("# Search Database by File")

uploaded_file = st.file_uploader("Upload a Case File", accept_multiple_files=False, type=['pdf'])

if uploaded_file:
    # st.write(uploaded_file.name)
    utils.empty_directory('prompt_data')
    utils.save_uploaded_file('prompt_data', uploaded_file)
    
    # print(os.path.join('prompt_data', uploaded_file.name))
    summary = ragger.summarise_input_file(os.path.join('prompt_data', uploaded_file.name))
    utils.empty_directory('prompt_data')
    # print(summary)
    
    ragger.create_db_link()
    relevant_file_names = ragger.find_relevant_files_from_prompt(summary)
    
    legible_file_names = []
    arguments = []
    legal_issues = []
    facts = []
    judge_names = []
    petitioners = []
    respondents = []
    for relevant_file_name in relevant_file_names:
        # Find the corresponding entry in 'TargetColumn'
        legible_file_names.append(df.loc[df['pdf_name'] == relevant_file_name, 'legible_name'].iloc[0])
        arguments.append(df.loc[df['pdf_name'] == relevant_file_name, 'Arguments'].iloc[0])
        legal_issues.append(df.loc[df['pdf_name'] == relevant_file_name, 'Legal_Issues'].iloc[0])
        facts.append(df.loc[df['pdf_name'] == relevant_file_name, 'Facts'].iloc[0])
        judge_names.append(df.loc[df['pdf_name'] == relevant_file_name, 'judges'].iloc[0]) 
        petitioners.append(df.loc[df['pdf_name'] == relevant_file_name, 'petitioners'].iloc[0])
        respondents.append(df.loc[df['pdf_name'] == relevant_file_name, 'respondant'].iloc[0])

    # st.write(legible_file_names)
    # Show the cards
        
    # chat_buttons = []

    N_cards_per_row = 1
    for n_row, row in enumerate(legible_file_names):
        i = n_row%N_cards_per_row
        if i==0:
            st.write("---")
            cols = st.columns(N_cards_per_row, gap="large")
        # draw the card
        with cols[n_row%N_cards_per_row]:
            st.markdown(f"### :green[{row}]")

            st.markdown("**Petitioner:**")
            st.markdown(f"{petitioners[n_row]}")
            st.markdown("**Respondants:**")
            st.markdown(f"{respondents[n_row]}")
            st.markdown("**Judges:**")
            st.markdown(f"{judge_names[n_row]}")

            with st.expander("Legal Issues"):
                st.write(legal_issues[n_row])
            with st.expander("Facts"):
                st.write(facts[n_row])
            with st.expander("Arguments"):
                st.write(arguments[n_row])

            # st.write(relevant_file_names[n_row])
            relevancy = ragger.query_single_file_data("Find relevancy of document with the prompt. You must find a relevancy no matter how small. prompt: " + summary, relevant_file_names[n_row])
            with st.expander("Relevancy"):
                st.write(relevancy)

            # chat_buttons.append(st.button("Find relevancy", key=n_row))
            # chat_buttons.append(st.button("Chat", key=n_row))
    # st.write("---")