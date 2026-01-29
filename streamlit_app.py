import streamlit as st
from tutor import ask_tutor

st.set_page_config(page_title="COSC 461 - AI Python Tutor", layout="centered")

st.title("COSC 461 • AI Python Tutor")
st.write("Ask any beginner Python question, request exercises, or paste code for feedback.")

# Keep convo memory in Streamlit session
if "history" not in st.session_state:
    st.session_state.history = None

if "last_reply" not in st.session_state:
    st.session_state.last_reply = ""

# Reset convo memory button
if st.button("Reset Tutor Conversation"):
    st.session_state.history = None
    st.success("Tutor memory cleared! Start a new conversation.")

# User input field
user_query = st.text_area(
    "Enter your question or code:",
    height=180,
    placeholder="Example: 'Explain Python loops' or 'Why is my code giving an error?'"
)

# When user clicks "Send"
if st.button("Send"):
    if user_query.strip():
        # Ask the tutor
        reply, meta, st.session_state.history = ask_tutor(
            user_query,
            conversation_history=st.session_state.history
        )

        st.session_state.last_reply = reply  # store reply

        # Display the tutor's response
        st.subheader("Tutor Response")
        st.code(reply, language="text")

        # Metadata (tokens + cost)
        st.subheader("Token & Cost Information")
        st.write(f"**Mode:** {meta['mode']}")
        st.write(f"**Prompt Tokens:** {meta['prompt_tokens']}")
        st.write(f"**Completion Tokens:** {meta['completion_tokens']}")
        st.write(f"**Total Tokens:** {meta['total_tokens']}")
        st.write(f"**Estimated Cost:** ${meta['estimated_cost']:.6f}")

    else:
        st.warning("Please enter something before clicking Send.")

# show last response if page refreshes
if st.session_state.last_reply and not st.button:
    st.subheader("Last Tutor Response")
    st.code(st.session_state.last_reply, language="text")
