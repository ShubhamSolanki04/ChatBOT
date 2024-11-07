from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

load_dotenv()  # Load environment variables

# Configure API
genai.configure(api_key='AIzaSyCayc50a3SUDeijDJdsiHWSbgRyWytt6FI') # Store API key securely in .env file

# Initialize the GenerativeModel for the Gemini Pro model
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Function to load Gemini Pro model and get responses with chat history
def get_gemini_response(conversation_history):
    # Combine all previous messages into a single prompt for context
    conversation_prompt = "\n".join([f"{role}: {text}" for role, text in conversation_history])
    response = chat.send_message(conversation_prompt, stream=True)
    return response

# Initialize our Streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("Gemini LLM Application")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# User input and submission button
user_input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

# Process the input and fetch response
if submit and user_input:
    st.session_state['chat_history'].append(("You", user_input))

    response = get_gemini_response(st.session_state['chat_history'])
    
    st.subheader("The Response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))

# Display the entire chat history
st.subheader("The Chat History is")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
