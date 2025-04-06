import streamlit as st
import pandas as pd

# Page title
st.set_page_config(page_title="Campaign Tracker")
st.title("📊 Campaign Tracker")

# Upload section
st.subheader("📤 Upload Campaign CSV")
uploaded_file = st.file_uploader("Choose a file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Convert 'Send Date' to datetime (accepts MM/DD/YYYY or M/D/YYYY)
    df["Send Date"] = pd.to_datetime(df["Send Date"], errors="coerce", dayfirst=False)

    # Save to session
    st.session_state["campaigns"] = df
    st.success("✅ Uploaded and parsed successfully.")
    st.write("📋 Uploaded Data:")
    st.dataframe(df)
else:
    # Default empty frame if nothing uploaded yet
    if "campaigns" not in st.session_state:
        st.session_state["campaigns"] = pd.DataFrame(columns=[
            "Channel", "Campaign Name", "Send Date", "Main Offer", "CTR (%)", "Open Rate (%)", "Notes"
        ])

# Add campaign form
with st.form("add_campaign"):
    st.subheader("➕ Add New Campaign")

    col1, col2 = st.columns(2)
    with col1:
        channel = st.selectbox("Channel", ["Email", "SMS", "Print"])
        name = st.text_input("Campaign Name")
        send_date = st.date_input("Send Date")

    with col2:
        offer = st.text_input("Main Offer")
        ctr = st.number_input("CTR (%)", step=0.1)
        open_rate = st.number_input("Open Rate (%)", step=0.1)

    notes = st.text_area("Notes", height=100)
    submit = st.form_submit_button("Add Campaign")

    if submit:
        new_row = pd.DataFrame([{
            "Channel": channel,
            "Campaign Name": name,
            "Send Date": pd.to_datetime(send_date),
            "Main Offer": offer,
            "CTR (%)": ctr,
            "Open Rate (%)": open_rate,
            "Notes": notes
        }])
        st.session_state["campaigns"] = pd.concat(
            [st.session_state["campaigns"], new_row], ignore_index=True
        )
        st.success("✅ Campaign added!")

# Filter by date
if not st.session_state["campaigns"].empty:
    st.subheader("📆 Filter Campaigns by Send Date")

    filter_date = st.date_input("Pick a date to view campaigns", value=pd.to_datetime("2025-06-01")).date()

    df = st.session_state["campaigns"].copy()
    df["Send Date"] = pd.to_datetime(df["Send Date"], errors="coerce")
    filtered = df[df["Send Date"].dt.date == filter_date]

    st.write("📁 Campaigns on", filter_date)
    st.dataframe(filtered)

    if filtered.empty:
        st.info("No campaigns found for that date.")
