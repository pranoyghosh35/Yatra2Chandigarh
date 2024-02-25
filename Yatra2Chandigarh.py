import os
import streamlit as st
import base64
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI
from langchain_community.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

def read_api_key(file_path):
    with open(file_path, 'r') as file:
        api_key = file.read().strip()  # Remove newline characters and leading/trailing whitespaces
    return api_key

def set_openai_api_key(api_key):
    os.environ["OPENAI_API_KEY"] = api_key

def load_docs(directory):
    loader = DirectoryLoader(directory, glob="**/*.txt")
    documents = loader.load()
    return documents

def split_documents_into_chunks(documents):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)
    return texts

def select_embeddings():
    return OpenAIEmbeddings()

def create_vectorstore(texts, embeddings):
    return Chroma.from_documents(texts, embeddings)

def create_retriever(db):
    return db.as_retriever(search_type='similarity', search_kwargs={"k": 2})

def create_qa_chain(llm, retriever):
    return RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=False)

def ask_setup():
    # Initialize an empty list to store chat history
    print("Please wait as we connect...",end="")

    # Read API key from api_key.txt file
    api_key_file = os.path.join(os.path.dirname(__file__), 'api_key.txt')
    api_key = read_api_key(api_key_file)

    # Set OpenAI API key in environment variable
    set_openai_api_key(api_key)
    #print("Setting api_key Done!")
    # Directory where text files are stored
    directory = "chandigarh_data/"

    # Load all the text files in the directory
    documents = load_docs(directory)

    # Split the documents into chunks
    texts = split_documents_into_chunks(documents)

    # Select embeddings
    embeddings = select_embeddings()

    # Create the vectorstore to use as the index
    db = create_vectorstore(texts, embeddings)

    # Expose the index in a retriever interface
    retriever = create_retriever(db)
    #print("Database Ready!")
    # Create instance to interact with OpenAI's language models
    llm = OpenAI()  # Instance to interact with OpenAI's language models. Default - GPT-3.5 Turbo

    # Create a chain to answer questions
    qa = create_qa_chain(llm, retriever)
    print("Ready to respond!")
    return qa
