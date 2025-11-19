import streamlit as st
from anthropic import Anthropic

st.title("Claude AI Chatbot")

# Load Claude API key from Streamlit Secrets
client = Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

# Default Claude model
if "claude_model" not in st.session_state:
    st.session_state["claude_model"] = "claude-3-sonnet-20240229"

# Chat message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new user message
if prompt := st.chat_input("What is up?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Claude streaming response
    with st.chat_message("assistant"):
        stream = client.messages.create(
            model=st.session_state["claude_model"],
            max_tokens=1024,
            stream=True,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
        )

        full_response = ""

        # Stream each token chunk
        for event in stream:
            if hasattr(event, "delta") and event.delta and hasattr(event.delta, "text"):
                chunk = event.delta.text
                full_response += chunk
                st.write(chunk)

    # Save full assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )
