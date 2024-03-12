import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Chat with documents",
    page_icon="👋",
)

st.write("# Chat with document")

st.sidebar.success("Select a demo above.")

df = pd.read_csv('metadata_doc4_gpt003s_0.csv')

# Show the dataframe (we'll delete this later)
# st.write(df)

# Use a text_input to get the keywords to filter the dataframe
text_search = st.text_input("Search Casefiles", value="")

# Filter the dataframe using masks
m1 = df["legible_name"].str.contains(text_search)
df_search = df[m1]

# Show the results, if you have a text_search
# if text_search:
#     st.write(df_search)

# Another way to show the filtered results
# Show the cards
N_cards_per_row = 3
if text_search:
    for n_row, row in df_search.reset_index().iterrows():
        i = n_row%N_cards_per_row
        if i==0:
            st.write("---")
            cols = st.columns(N_cards_per_row, gap="large")
        # draw the card
        with cols[n_row%N_cards_per_row]:
            st.caption(f"{row['legible_name'].strip()}")