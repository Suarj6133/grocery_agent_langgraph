import streamlit as st
import pandas as pd
from agent import ask_agent
from custom_tools import get_reorder_data


st.title("My first Agent - Grocery Agent")

# ==========================================
# CHAT SECTION
# ==========================================
user_input = st.text_input("Ask your question")

if st.button("Submit"):
    if user_input:
        try:
            answer = ask_agent(user_input)
            st.success(answer)
        except Exception as e:
            st.error(f"Error: {e}")

# ==========================================
# RE-ORDER SECTION
# ==========================================
st.markdown("---")
st.subheader("SKUs Eligible for Re-Order")
st.caption("Re-order criteria: Inventory / Daily Order Qty < 10")

# Get data from custom_tools (no direct DB connection here)
reorder_data = get_reorder_data()

if not reorder_data:
    st.info("No SKUs are currently eligible for re-order.")
else:
    # Table header
    cols = st.columns([1, 1, 1.5, 1.5, 1])
    cols[0].markdown("**SKU**")
    cols[1].markdown("**Inventory**")
    cols[2].markdown("**Daily Orders**")
    cols[3].markdown("**Days of Stock**")
    cols[4].markdown("**Action**")

    # Table rows with re-order button per SKU
    for row in reorder_data:
        cols = st.columns([1, 1, 1.5, 1.5, 1])
        cols[0].write(row["SKU"])
        cols[1].write(row["Inventory"])
        cols[2].write(row["Daily Orders"])
        cols[3].write(row["Days of Stock"])
        if cols[4].button("Re-Order", key=f"reorder_{row['SKU']}"):
            st.success(f"Re-order placed for {row['SKU']}!")
