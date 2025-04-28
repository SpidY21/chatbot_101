import streamlit as st
import requests
import json


OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
MODEL = "mistralai/mistral-tiny" 

def chatbot(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        return f"Error communicating with the API: {e}"
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        return f"Error processing the API response: {e}"

# --- Streamlit UI ---
st.title("AI Powered Chatbot")
st.markdown("Type your query and press Enter.")

# Initialize chat history in Streamlit Session State
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat messages from history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
if prompt := st.chat_input("Your message"):
    # Add user message to chat history
    st.session_state["messages"].append({"role": "user", "content": prompt})
    # Display user message in the chat container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from the chatbot
    bot_response = chatbot(prompt)

    # Add bot response to chat history
    st.session_state["messages"].append({"role": "assistant", "content": bot_response})
    # Display bot response in the chat container
    with st.chat_message("assistant"):
        st.markdown(bot_response)
        
