#pip install langchain
import os
import openai
import sys

# load pdf pages
def load_pdf_pages():

    from langchain.document_loaders import PyPDFLoader
    loader = PyPDFLoader("input-docs/MachineLearning-Lecture01.pdf")
    pages = loader.load()

    page0 = pages[0]
    page1 = pages[1]

    print("page metadata: \n", page0.metadata)

# load notiondb
def load_notion_db():
    from langchain.document_loaders import NotionDirectoryLoader
    notionloader = NotionDirectoryLoader("notiondb/Notion_DB")
    docs = notionloader.load()  
    print("notiondb metadata: \n", docs.metadata)



def load_youtube_data():

    from langchain.document_loaders.generic import GenericLoader
    from langchain.document_loaders.parsers import OpenAIWhisperParser
    from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader

    print("load youtube data")   

    url="https://www.youtube.com/watch?v=jGwO_UgTS7I"
    save_dir="docs/youtube/"
    loader = GenericLoader(YoutubeAudioLoader([url],save_dir), OpenAIWhisperParser())
    docs = loader.load()

    #print("youtube page content \n", docs[0].page_content[0:500])


# main
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ['OPENAI_API_KEY']
sys.path.append('../..')


#load_pdf_pages()
#load_notion_db()
load_youtube_data()








