import os

import chromadb 
from langchain.text_splitter import CharacterTextSplitter
from chromadb.utils import embedding_functions

default_ef = embedding_functions.DefaultEmbeddingFunction()

client = chromadb.PersistentClient(path=os.path.join(os.getcwd(), "vector_database"))

collection = client.get_or_create_collection(
    name="chroma_collection",        
    embedding_function = default_ef,
    metadata={
        "hnsw:space": "cosine",
    },
)


text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=1)