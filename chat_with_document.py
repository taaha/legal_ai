import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Chat with documents",
    page_icon="👋",
)

st.write("# Chat with document")

st.sidebar.success("Select a demo above.")

df = pd.read_csv('metadata_doc4_gpt003s_0.csv')

df_no_duplicates = df.drop_duplicates(subset=['pdf_name'])

# Use a text_input to get the keywords to filter the dataframe
text_search = st.text_input("Search Casefiles", value="")

names_list = df_no_duplicates['legible_name'].tolist()

# Filter the list based on the search text
filtered_names = [name for name in names_list if text_search.lower() in name.lower()]

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