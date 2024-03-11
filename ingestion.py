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

Settings.embed_model = OpenAIEmbedding()

openai.api_key = os.environ["OPENAI_API_KEY"]
# embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
documents = SimpleDirectoryReader("./documents").load_data()
db = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = db.get_or_create_collection("quickstart")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)