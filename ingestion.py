from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex, Document
from llama_index.core.vector_stores import MetadataFilters, ExactMatchFilter
from llama_index.core import StorageContext
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
from llama_index.core import StorageContext
import tiktoken
from llama_index.core.callbacks import CallbackManager, TokenCountingHandler
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from IPython.display import Markdown, display
import chromadb
import pandas as pd
import chromadb
import openai
from tqdm import tqdm
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


token_counter = TokenCountingHandler(
    tokenizer=tiktoken.encoding_for_model("gpt-3.5-turbo").encode
)

Settings.callback_manager = CallbackManager([token_counter])

### Loading Documents
print("loading documents")
documents = SimpleDirectoryReader("documents_44_v0").load_data()


print("reforming metadata")
### Metadata reformation
documents_with_metadata = []
for document in tqdm(documents):
    documents_with_metadata.append(Document(text=document.text, metadata={
                                                                            "page": document.metadata["page_label"], 
                                                                            "pdf_name": document.metadata["file_name"]
                                                                        }))
    

### Saving metadata to df
pdf_names = []
pages = []
doc_ids = []

for doc in tqdm(documents_with_metadata):
    pdf_names.append(doc.metadata["pdf_name"])
    pages.append(doc.metadata["page"])
    doc_ids.append(doc.id_)
# Create a DataFrame from the lists
df = pd.DataFrame({
    'pdf_name': pdf_names,
    'page': pages,
    'id': doc_ids
})
# Adding a new column 'legible_name' with '_' replaced by space in 'pdf_name'
df['legible_name'] = df['pdf_name'].str.replace('_', ' ')
# Convert the DataFrame to a CSV file
csv_file_path = 'metadata_doc44_gpt003s_0.csv'
df.to_csv(csv_file_path, index=False)


### Create chromadb
print("creating chroma")
db = chromadb.PersistentClient(path="./chroma_db_doc44_gpt003s_metadata_0_c")
chroma_collection = db.get_or_create_collection("quickstart")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents_with_metadata, storage_context=storage_context
)


print("running detail extraction pipeline")
### Detail extraction pipeline
df_no_duplicates = df.drop_duplicates(subset=['pdf_name'])
# Iterating over rows
for i, row in tqdm(df_no_duplicates.iterrows()):
    filters = MetadataFilters(filters=[ExactMatchFilter(key="pdf_name", value=row['pdf_name'])])
    query_engine = index.as_query_engine(filters=filters)

    legal_issues_response = query_engine.query("What is the legal issue in case, explain in detail")
    df_no_duplicates.at[i, 'Legal_Issues'] = legal_issues_response.response
    
    facts_response = query_engine.query("What are the facts of the case?, write pointwise")
    df_no_duplicates.at[i, 'Facts'] = facts_response.response

    arguments_response = query_engine.query("What are the arguments in the case?, write pointwise")
    df_no_duplicates.at[i, 'Arguments'] = arguments_response.response

df_no_duplicates.to_csv("metadata_doc44_gpt003s_0_no_duplicates.csv")

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

for i, row in tqdm(df_no_duplicates.iterrows()):
    # print(f"Index: {i}")
    # if i==1008:
    # df_no_duplicates.at[index, 'NewColumn'] = 1
    # print(row['pdf_name'])
    documents = SimpleDirectoryReader(input_files=[f"./documents_44_v0/{row['pdf_name']}"]).load_data()

    user_prompt = "\n In the above text, write the names of judges sitting in the bench on this case. Answer should only contain name of Judges"
    gpt_prompt = documents[0].text + documents[1].text + user_prompt

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": gpt_prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )

    df_no_duplicates.at[i, 'judges'] = chat_completion.choices[0].message.content

    user_prompt = "\n In the above text, write the names of petitioner on this case. Answer should only contain petitioners"
    gpt_prompt = documents[0].text + documents[1].text + user_prompt

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": gpt_prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )

    df_no_duplicates.at[i, 'petitioners'] = chat_completion.choices[0].message.content

    user_prompt = "\n In the above text, write the names of respondants on this case. Answer should only contain respondant"
    gpt_prompt = documents[0].text + documents[1].text + user_prompt

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": gpt_prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )

    df_no_duplicates.at[i, 'respondant'] = chat_completion.choices[0].message.content

df_no_duplicates.to_csv("metadata_doc44_gpt003s_0_detailed.csv")


print(
    "Embedding Tokens: ",
    token_counter.total_embedding_token_count,
    "\n",
    "LLM Prompt Tokens: ",
    token_counter.prompt_llm_token_count,
    "\n",
    "LLM Completion Tokens: ",
    token_counter.completion_llm_token_count,
    "\n",
    "Total LLM Token Count: ",
    token_counter.total_llm_token_count,
    "\n",
)