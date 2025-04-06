import streamlit as st
import pandas as pd

# Set the page title
st.set_page_config(page_title="Campaign Tracker")

st.title("📊 Campaign Tracker")

# Initialize the campaign database
if "campaigns" not in st.session_state:
    st.session_state.campaigns = pd.DataFrame(columns=[
        "Channel", "Campaign Name", "Send Date", "Main Offer", "CTR (%)", "Open Rate (%)", "Notes"
    ])

# Campaign input form
with st.form("add_campaign"):
    st.subheader("➕ Add a New Campaign")
    col1, col2 = st.columns(2)

    with col1:
        channel = st.selectbox("Channel", ["Email", "SMS", "Print"])
        name = st.text_input("Campaign Name")
        date = st.date_input("Send Date")

    with col2:
        offer = st.text_input("Main Offer")
        ctr = st.number_input("CTR (%)", step=0.1)
        open_rate = st.number_input("Open Rate (%)", step=0.1)
    
    notes = st.text_area("Notes", height=100)
    submitted = st.form_submit_button("Add Campaign")

    if submitted:
        new_campaign = {
            "Channel": channel,
            "Campaign Name": name,
            "Send Date": date,
            "Main Offer": offer,
            "CTR (%)": ctr,
            "Open Rate (%)": open_rate,
            "Notes": notes
        }
        st.session_state.campaigns = st.session_state.campaigns.append(new_campaign, ignore_index=True)
        st.success("✅ Campaign added!")

# Display the data
st.subheader("📁 All Campaigns")
st.dataframe(st.session_state.campaigns)