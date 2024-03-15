import streamlit as st
import pandas as pd
from ragger import ragger

st.set_page_config(
    page_title="Legal AI",
    page_icon="🤖",
)

ragger=ragger()

df = pd.read_csv('metadata_doc4_gpt003s_0_detailed.csv')

st.write("# Search Database by Prompt")

# Use a text_input to get the keywords to filter the dataframe
prompts_search = st.text_input("Enter prompt", value="")

if prompts_search:
    ragger.create_db_link()
    relevant_file_names = ragger.find_relevant_files_from_prompt(prompts_search)
    
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
            relevancy = ragger.query_single_file_data("How is the document related to the prompt: " + prompts_search, relevant_file_names[n_row])
            with st.expander("Relevancy"):
                st.write(relevancy)
    
    st.write("---")