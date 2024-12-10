import streamlit as st
import requests
import json

# Base URL of the API
BASE_URL = "http://127.0.0.1:5000"

# Function to load data into the vector database
def load_data(user_name, data):
    url = f"{BASE_URL}/load"
    payload = {
        "user_name": user_name,
        "data": data
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return True, response.json().get("message")
    else:
        return False, response.json().get("error", "Unknown error occurred")

# Function to perform chat with the vector database
def chat(user_name, query):
    url = f"{BASE_URL}/chat"
    payload = {
        "user_name": user_name,
        "query": query
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return True, response.json()
    else:
        return False, response.json().get("error", "Unknown error occurred")

# Streamlit App
st.title("Vector Database Semantic Search")
st.write("Upload JSON data, load it into the vector database, and perform semantic search using natural language queries.")

# Sidebar for User Info
st.sidebar.title("User Information")
user_name = st.sidebar.text_input("Enter your username", "default_user")

# Upload JSON Data
st.header("Step 1: Upload JSON Data")
uploaded_file = st.file_uploader("Upload a JSON file", type=["json"])

if uploaded_file:
    try:
        data = json.load(uploaded_file)
        st.json(data)  # Display the uploaded data
        if st.button("Load Data"):
            success, message = load_data(user_name, data)
            if success:
                st.success(f"Data loaded successfully: {message}")
            else:
                st.error(f"Error loading data: {message}")
    except Exception as e:
        st.error(f"Invalid JSON file: {str(e)}")

# Chat with Data
st.header("Step 2: Chat with Your Data")
query = st.text_input("Enter your question")
if st.button("Ask"):
    if query:
        success, response = chat(user_name, query)
        if success:
            st.write("### Response")
            st.write(response.get("response"))
            st.write("### Matched Data")
            for matched_data in response.get("matched_data", []):
                st.write(f"- {matched_data}")
        else:
            st.error(f"Error during chat: {response}")
    else:
        st.warning("Please enter a question before clicking 'Ask'.")
