from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.vector_stores.types import MetadataFilters, ExactMatchFilter
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
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

    def create_db_link(self):
        db2 = chromadb.PersistentClient(path="./chroma_db_doc44_gpt003s_metadata_0_c")
        chroma_collection = db2.get_or_create_collection("quickstart")
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        self.index = VectorStoreIndex.from_vector_store(
            vector_store,
        )

    def query_data(self, prompt):
        # Query Data from the persisted index
        # query_engine = self.index.as_query_engine()
        self.chat_engine = self.index.as_chat_engine(chat_mode="condense_question", verbose=True)
        # response = query_engine.query(prompt + "\n Answer in detail")
        response = self.chat_engine.chat(prompt)
        return response.response
    
    def query_single_file_data(self, prompt, pdf_name):
        # print(pdf_name)
        filters = MetadataFilters(filters=[ExactMatchFilter(key="pdf_name", value=pdf_name)])
        query_engine = self.index.as_query_engine(filters=filters)
        # self.chat_engine = self.index.as_chat_engine(chat_mode="condense_question", verbose=True, filters=filters)
        # response = self.chat_engine.chat(prompt)
        response = query_engine.query(prompt)
        # print(response.source_nodes)
        # print(response.source_nodes)
        return response.response
    
    def find_relevant_files_from_prompt(self, prompt):
        # configure retriever
        retriever = VectorIndexRetriever(
            index=self.index,
            similarity_top_k=2,
            # similarity_cutoff=0.5
        )
        node_postprocessors = [
        SimilarityPostprocessor(similarity_cutoff=0.5)
        ]
        query_engine = RetrieverQueryEngine.from_args(
            retriever, node_postprocessors=node_postprocessors, response_mode="no_text"
        )
        response = query_engine.query(prompt)

        file_names = set()
        for source_node in response.source_nodes:
            file_names.add(source_node.metadata['pdf_name'])
        return list(file_names)
    
    def summarise_input_file(self, filepath):
        documents = SimpleDirectoryReader(
        input_files=[filepath]
            ).load_data()

        if len(documents) > 20:
            documents = documents[:20]

        index = VectorStoreIndex.from_documents(documents)
        query_engine = index.as_query_engine()

        response = query_engine.query("Summarize this document")
        
        return response.response