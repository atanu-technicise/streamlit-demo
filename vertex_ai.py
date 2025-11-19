import streamlit as st
import vertexai
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel

# --------------------------
# Load Credentials
# --------------------------
creds_path = st.secrets["google"]["credentials_path"]
project_id = st.secrets["google"]["project_id"]
location = st.secrets["google"]["location"]

credentials = service_account.Credentials.from_service_account_file(creds_path)

# --------------------------
# Initialize Vertex AI
# --------------------------
vertexai.init(
    project=project_id,
    location=location,
    credentials=credentials
)

# Load the Gemini Model
model = GenerativeModel("gemini-pro")

# --------------------------
# Streamlit UI
# --------------------------
st.title("💬 Gemini Chatbot (Vertex AI)")
st.write("A simple ChatGPT-like chatbot using Google Gemini.")

# Initialize session state chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display history
for msg in st.session_state.chat_history:
    role = "🧑 You:" if msg["role"] == "user" else "🤖 Gemini:"
    st.write(f"**{role}** {msg['content']}")

# User Input
user_input = st.text_input("Ask something:", "")

# --------------------------
# When user sends message
# --------------------------
if user_input:
    # Add user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Call Gemini API
    response = model.generate_content(user_input)
    bot_reply = response.text

    # Add bot message
    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})

    # Refresh UI
    st.rerun()
