from langchain.chains import RetrievalQA
from langchain_openai import OpenAI
from langchain_community.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# Function to load documents from the directory
def load_docs(directory):
    loader = DirectoryLoader(directory, glob="**/*.txt")
    documents = loader.load()
    return documents

# Function to split documents into chunks for embedding
def split_documents_into_chunks(documents):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)
    return texts

# Function to select the OpenAI embeddings
def select_embeddings(api_key):
    return OpenAIEmbeddings(openai_api_key=api_key)

# Function to create the Chroma vectorstore
def create_vectorstore(texts, embeddings):
    return Chroma.from_documents(texts, embeddings)

# Function to create a retriever for similarity-based searches
def create_retriever(db):
    return db.as_retriever(search_type='similarity', search_kwargs={"k": 2})

# Function to create the question-answer chain
def create_qa_chain(llm, retriever):
    return RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=False)

# Main function to set up the QA system
def ask_setup(api_key):
    print("Please wait as we connect...", end="")

    # Directory where text files are stored
    directory = "backend/chandigarh_data"

    # Load all the text files in the directory
    documents = load_docs(directory)

    # Split the documents into chunks
    texts = split_documents_into_chunks(documents)

    # Select embeddings
    embeddings = select_embeddings(api_key)

    # Create the vectorstore to use as the index
    db = create_vectorstore(texts, embeddings)

    # Expose the index in a retriever interface
    retriever = create_retriever(db)

    # Create instance to interact with OpenAI's language models
    llm = OpenAI(openai_api_key=api_key)  # Pass the API key to OpenAI

    # Create a chain to answer questions
    qa = create_qa_chain(llm, retriever)
    
    print("Ready to respond!")
    return qa
