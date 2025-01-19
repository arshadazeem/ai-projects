from dotenv import load_dotenv
import os
import streamlit as st
import openai
import logging as log
import uuid
import loadprops

from PyPDF2 import PdfReader
from docx import Document
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SimpleField, SearchableField
from azure.core.exceptions import ResourceNotFoundError
from azure.core.credentials import AzureKeyCredential


# Load variables from .env file
load_dotenv()

# Set up Azure OpenAI credentials
openai.api_type = os.getenv("OPEN_AI_API_TYPE")  
openai.azure_endpoint = os.getenv("OPEN_AI_API_ENDPOINT_CHAT") 
openai.api_key = os.getenv("OPEN_AI_API_KEY_CHAT")
openai.api_version = os.getenv("OPEN_AI_API_VERSION_CHAT")    # "2024-05-01-preview"  


# Set up Azure Search credentials
azure_ai_search_service_name = os.getenv("AZURE_AI_SEARCH_SERVICE_NAME")
azure_ai_search_service_endpoint = os.getenv("AZURE_AI_SEARCH_SERVICE_ENDPOINT")
azure_ai_search_index_name = os.getenv("AZURE_AI_SEARCH_INDEX_NAME")

# Search API Key object
azure_ai_search_api_key = AzureKeyCredential(os.getenv("AZURE_AI_SEARCH_API_KEY"))

search_client = SearchClient(endpoint=azure_ai_search_service_endpoint, index_name=azure_ai_search_index_name, credential=azure_ai_search_api_key)

# Streamlit app configuration
st.title("AI Chatbot with Azure OpenAI and Azure Search")

# generate greeting from user message
def generate_greeting(user_message):
    response = openai.chat.completions.create(
            model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a friendly chatbot."},
            {"role": "user", "content": user_message}
        ],
        max_tokens=500,
        temperature=0.7,
    )
    return response.choices[0].message.content

# extract document content from file
def extract_content(file):
    if file.name.endswith(".pdf"):
        reader = PdfReader(file)
        return "\n".join([page.extract_text() for page in reader.pages])
    elif file.name.endswith(".docx"):
        doc = Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    return None

# def create_index():
#     index_client = SearchIndexClient(endpoint=azure_ai_search_service_endpoint, credential=azure_ai_search_api_key)
#     fields = [
#         SimpleField(name="id", type="Edm.String", key=True),
#         SearchableField(name="content", type="Edm.String"),
#     ]
#     index = SearchIndex(name=azure_ai_search_index_name, fields=fields)
#     index_client.create_index(index)

#  Create the index if it doesn't exist
def create_index_if_not_exists():
    # Initialize the SearchIndexClient
    index_client =  SearchIndexClient(endpoint=azure_ai_search_service_endpoint, credential=azure_ai_search_api_key) 
 
    try:
        # Check if the index already exists
        index_client.get_index(azure_ai_search_index_name)
        print(f"Index '{azure_ai_search_index_name}' already exists. Skipping creation.")
    except ResourceNotFoundError:
        # Create the index if it doesn't exist
        print(f"Index '{azure_ai_search_index_name}' does not exist. Creating index...")
        fields = [
            SimpleField(name="id", type="Edm.String", key=True),
            SearchableField(name="content", type="Edm.String"),
        ]
        index = SearchIndex(name=azure_ai_search_index_name, fields=fields)
        index_client.create_index(index)
        print(f"Index '{azure_ai_search_index_name}' created successfully.")


# upload document
def upload_document(content, doc_id):

    create_index_if_not_exists()

    document = {"id": doc_id, "content": content}
    search_client.upload_documents(documents=[document])
    print(f"document wiuth id {doc_id} uploaded successfully")

# search documents based on query
def search_documents(query):    
    results = search_client.search(query)
    return "\n".join([doc["content"] for doc in results])

# answer user query based on documents uploaded by user
def answer_query(user_query):
    retrieved_docs = search_documents(user_query)
    response = openai.chat.completions.create(
            model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a funny but friendly AI assistant that answers questions based on uploaded documents."},
             {"role": "user", "content": f"The user uploaded documents contain the following:\n{retrieved_docs}"},
            {"role": "user", "content": f"Answer this query the user asked based on the documents they uploaded: {user_query}"}
        ],
        max_tokens=2500,
        temperature=0.7,
    )
    return response.choices[0].message.content

# Streamlit UI - Greetings
user_message = st.text_input("Say something:")
if user_message:
    st.write("Chatbot:", generate_greeting(user_message))

# File Upload
uploaded_file = st.file_uploader("Upload your document", type=["pdf", "docx"])
if uploaded_file:
    doc_content = extract_content(uploaded_file)
    st.write("Completed Document content extraction!")
   # st.text(doc_content)
    mydoc_id = str(uuid.uuid4())
    upload_document(doc_content, doc_id=mydoc_id)


# Query Input
user_query = st.text_input("Ask a question about the document:")
if user_query:
    #retrieved_docs = search_documents(user_query)
    #st.write("Retrieved documents:", retrieved_docs)
    answer = answer_query(user_query)
    st.write("Answer:", answer)







