from dotenv import load_dotenv
import os
from openai import AzureOpenAI

# Load variables from .env file
load_dotenv()


openai_api_key = os.getenv('OPEN_AI_API_KEY_COMPLETIONS')
openai_api_version = os.getenv('OPEN_AI_API_VERSION_COMPLETIONS')
openai_azure_endpoint = os.getenv('OPEN_AI_API_ENDPOINT_COMPLETIONS')

client = AzureOpenAI(api_key=openai_api_key, api_version=openai_api_version, azure_endpoint=openai_azure_endpoint)
    
deployment_name="davinci-002" #This will correspond to the custom name you chose for your deployment when you deployed a model. Use a gpt-35-turbo-instruct deployment. 

embeddings_input = "Zain Azeem who is 11 years old, plays as a striker or center mid for Loudoun Soccer. His brother Zoaib is almost 8 years old. He is learning soccer and loves to draw. They both are taekwondo students"

myembedding = client.embeddings.create(input=embeddings_input, model=deployment_name).data[0].embedding

print(myembedding)


# Send a completion call to generate an answer
print('Sending a test completion job')
prompt = 'Write a tagline for an bike shop.'
response = client.completions.create(model=deployment_name, prompt=prompt, max_tokens=100)
print(prompt+response.choices[0].text)