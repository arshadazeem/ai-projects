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
openai.api_version = os.getenv("OPEN_AI_API_VERSION_CHAT")