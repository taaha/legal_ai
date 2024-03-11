from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
import chromadb
import openai
import os
import utils
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

openai.api_key = os.environ["OPENAI_API_KEY"]

class ragger():
    def __init__(self):
        Settings.embed_model = OpenAIEmbedding()

    def reingest(self):
        utils.delete_directory("./chroma_db")
        # utils.create_directory("./chroma_db")
        documents = SimpleDirectoryReader("./documents").load_data()
        db = chromadb.PersistentClient(path="./chroma_db")
        chroma_collection = db.get_or_create_collection("quickstart")
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        self.index = VectorStoreIndex.from_documents(
            documents, storage_context=storage_context
        )


    def create_db_link(self):
        # if os.path.exists("./chroma_db"):
            # try:
        db2 = chromadb.PersistentClient(path="./chroma_db")
        chroma_collection = db2.get_or_create_collection("quickstart")
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        self.index = VectorStoreIndex.from_vector_store(
            vector_store,
        )
            # except Exception as e:
            #     print(e)

    def query_data(self, prompt):
        # Query Data from the persisted index
        # query_engine = self.index.as_query_engine()
        chat_engine = self.index.as_chat_engine(chat_mode="condense_question", verbose=True)
        # response = query_engine.query(prompt + "\n Answer in detail")
        response = chat_engine.chat(prompt + "\n Answer in detail")
        return response.response