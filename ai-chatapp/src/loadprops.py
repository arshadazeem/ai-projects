from dotenv import load_dotenv
import os
import openai
import logging as log

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