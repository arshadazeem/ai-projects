import logging as log
import os
from dotenv import load_dotenv

from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
#from azure.search.documents.indexes.models import SearchIndex, SimpleField, SearchableField
#from azure.core.exceptions import ResourceNotFoundError
from azure.core.credentials import AzureKeyCredential

# Load variables from .env file
load_dotenv()

# Set up Azure Search credentials
azure_ai_search_service_name = os.getenv("AZURE_AI_SEARCH_SERVICE_NAME")
azure_ai_search_service_endpoint = os.getenv("AZURE_AI_SEARCH_SERVICE_ENDPOINT")
azure_ai_search_index_name = os.getenv("AZURE_AI_SEARCH_INDEX_NAME")

# Search API Key object
azure_ai_search_api_key = AzureKeyCredential(os.getenv("AZURE_AI_SEARCH_API_KEY"))

search_client = SearchClient(endpoint=azure_ai_search_service_endpoint, index_name=azure_ai_search_index_name, credential=azure_ai_search_api_key)

search_index_client = SearchIndexClient(endpoint=azure_ai_search_service_endpoint, credential=azure_ai_search_api_key) 


 # Deletes the specified index
def delete_index():
    print(f"Deleting index {azure_ai_search_index_name}")
    search_index_client.delete_index(azure_ai_search_index_name)
    print(f"Index ${azure_ai_search_index_name} deleted!")

# Delete all documents from the index
delete_index()