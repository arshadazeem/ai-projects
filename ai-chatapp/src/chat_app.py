from dotenv import load_dotenv
import os
import streamlit as st
import openai
import logging as log

# Load variables from .env file
load_dotenv()

# Set up Azure OpenAI credentials
openai.api_type = os.getenv("OPEN_AI_API_TYPE")  
openai.azure_endpoint = os.getenv("OPEN_AI_API_ENDPOINT_CHAT") 

openai.api_key = os.getenv("OPEN_AI_API_KEY_CHAT")
openai.api_version = os.getenv("OPEN_AI_API_VERSION_CHAT")    # "2024-05-01-preview"  

# Streamlit app configuration
st.set_page_config(page_title="Chat Interface with Azure OpenAI", layout="wide")

# Session state to store conversation history
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# Function to call Azure OpenAI model
def query_openai(messages):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",  # Replace with your Azure OpenAI deployment name
            messages=messages,
            max_tokens=500,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# Streamlit UI
st.title("Chat Interface with Azure OpenAI")
st.markdown("Powered by Azure OpenAI and Streamlit")

# Display conversation
for message in st.session_state["messages"]:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}")
    elif message["role"] == "assistant":
        st.markdown(f"**Assistant:** {message['content']}")

# User input
user_input = st.text_input("Enter your message:", key="user_input")

# Handle user input
if st.button("Send") and user_input:
    # Add user message to session state
    st.session_state["messages"].append({"role": "user", "content": user_input})



    # Query Azure OpenAI
    assistant_reply = query_openai(st.session_state["messages"])

    

    # Add assistant message to session state
    st.session_state["messages"].append({"role": "assistant", "content": assistant_reply})

    print("****************")

    print(st.session_state["messages"])

    print("****************")

    # Clear user input
    st.text_input("Enter your message:", value="", on_change=None)

# Clear chat history
if st.button("Clear Chat"):
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
