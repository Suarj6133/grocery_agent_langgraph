import streamlit as st
from agent import ask_agent


st.title("Langgraph - AI agent _ Replit")
user_input = st.text_input("ask your question")

#submit button
if st.button("Submit"):
    if user_input:
        try:
            answer = ask_agent(user_input)
            st.success(answer)
        except Exception as e:
            st.error(f"error is {e}")



