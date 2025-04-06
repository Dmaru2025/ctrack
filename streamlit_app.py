import streamlit as st
import pandas as pd

st.set_page_config(page_title="Campaign Tracker")

st.title("📊 Campaign Tracker")

# Upload CSV
st.subheader("📤 Upload Campaign File (CSV)")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Parse M/D/YYYY style dates
    df["Send Date"] = pd.to_datetime(df["Send Date"], format="%m/%d/%Y", errors="coerce")

    st.session_state.campaigns = df
    st.success("✅ Campaign data uploaded successfully!")

    # Debug output
    st.write("📋 Uploaded Campaigns:")
    st.dataframe(df)
    st.write("📅 Dates in data:", df["Send Date"].dt.date.unique())

# Initialize empty if needed
if "campaigns" not in st.session_state:
    st.session_state.campaigns = pd.DataFrame(columns=[
        "Channel", "Campaign Name", "Send Date", "Main Offer", "CTR (%)", "Open Rate (%)", "Notes"
    ])

# Form to add a campaign
with st.form("add_campaign"):
    st.subheader("➕ Add Campaign")
    col1, col2 = st.columns(2)

    with col1:
        channel = st.selectbox("Channel", ["Email", "SMS", "Print"])
        name = st.text_input("Campaign Name")
        date = st.date_input("Send Date")

    with col2:
        offer = st.text_input("Main Offer")
        ctr = st.number_input("CTR (%)", step=0.1)
        open_rate_val = st.number_input("Open Rate (%)", step=0.1)  # renamed to avoid conflict

    notes = st.text_area("Notes")
    submitted = st.form_submit_button("Add Campaign")

    if submitted:
        new_row = {
            "Channel": channel,
            "Campaign Name": name,
            "Send Date": pd.to_datetime(date),
            "Main Offer": offer,
            "CTR (%)": ctr,
            "Open Rate (%)": open_rate_val,
            "Notes": notes
        }
        st.session_state.campaigns = pd.concat([
            st.session_state.campaigns,
            pd.DataFrame([new_row])
        ], ignore_index=True)
        st.success("✅ Campaign added!")

# Filter by date
if not st.session_state.campaigns.empty:
    st.subheader("📆 Filter by Date")
    filter_date = st.date_input("Select date to view campaigns", value=pd.to_datetime("2025-06-01")).date()

    # Convert and filter
    df = st.session_state.campaigns.copy()
    df["Send Date"] = pd.to_datetime(df["Send Date"], errors="coerce")

    filtered = df[df["Send Date"].dt.date == filter_date]

    st.subheader("📁 Campaigns on Selected Date")
    st.dataframe(filtered)

    if filtered.empty:
        st.warning("No campaigns found on that date.")
