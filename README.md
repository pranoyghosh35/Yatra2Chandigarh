# Yatra2Chandigarh

<p align="center">
  <img src="chandigarh_data/chandigarh_hand_symbol.jpg" alt="Open Hand" width="25%" height="25%">
</p>

Yatra2Chandigarh is a chatbot developed as a course project during the Plaksha Tech Leaders Fellowship 2023-24. It is designed to provide information and answer questions about the city of Chandigarh.

## Introduction

Whether you are a tourist exploring the "City Beautiful," a business traveler attending meetings and conferences, or someone considering moving to Chandigarh, Yatra2Chandigarh is here to assist you. Leveraging web-information (as of 11th Feb 2024) from the Chandigarh Industrial and Tourism Development Corporation Limited (CITCO), this virtual guide offers insights into various aspects of Chandigarh, including tourist attractions, local cuisine, accommodation, transportation, and more.

## Usage

If you clone from github, recommend creating a virtual environment and use 'requirements.txt' to install all dependencies. 
Please copy securely your OpenAI key in 'api_key.txt' (don't share publicly)
Finally 'streamlit run run_me.py'.

If you are unsure of its capabilities, try asking about itself and what topics or example questions it can answer.

## Example Questions

- What are the top tourist attractions in Chandigarh?
- What is the weather like in Chandigarh?
- What are the best restaurants to try in Chandigarh?
- What is the history of Chandigarh?
- What are the best shopping areas in Chandigarh?
- What are the popular festivals and events in Chandigarh?
- What are some unique cultural customs in Chandigarh?
- etc.

## Implementation Details

![Putting everything together](https://av-eks-lekhak.s3.amazonaws.com/media/__sized__/article_images/4_J5W8UB8-thumbnail_webp-600x300.webp)

### Web Scraping and Data Processing

We loaded web-scraped data available as several *.txt files kept inside the 'chandigarh_data' directory, tokenized them using CharacterTextSplitter from langchain.text_splitter, and embedded them into vectors using OpenAIEmbeddings. These vectors were then stored in Chroma database.

### Chroma Database

Chroma DB is an open-source vector storage system (vector database) designed for storing and retrieving vector embeddings. Its primary function is to store embeddings with associated metadata for subsequent use by extensive language models.

**Reference:** [Chroma Database](https://python.langchain.com/docs/integrations/vectorstores/chroma)

### Combining RAG, Langchain, and Vector Databases

We developed a retrieval-augmented AI system that is both generative and retrieval-based by combining the strength of OpenAI’s GPT models, LangChain, and Pinecone Vector Databases. This system can retrieve and use particular pieces of information in addition to producing creative and human-like text.

**Reference:** [OpenAI Integration](https://python.langchain.com/docs/integrations/platforms/openai)

### Implementing Question Answering in LangChain

There are different ways to do question answering in LangChain. We used the ConversationalRetrievalChain, which offers a chat history component and is an advancement of RetriervalQAChat.

**Reference:** [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)

## Future Development Scope

**Keeping it up-to-date is easy for anyone:** Create a plain text file containing the latest information about Chandigarh and save it to the unzipped 'chandigarh_data/' folder. It is better if you can format the new information in small paragraphs and add sample questions below it.

## Enjoy!!
YouTube: https://youtu.be/35RFzvTBy6o,
Write to pranoy.ghosh.tlp23@plaksha.edu.in for feedback.
