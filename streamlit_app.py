import streamlit as st
import pandas as pd

# Set the page title
st.set_page_config(page_title="Campaign Tracker")

st.title("📊 Campaign Tracker")

# Upload CSV
st.subheader("📤 Upload Campaign File (CSV)")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    uploaded_df = pd.read_csv(uploaded_file)

    # Force 'Send Date' to datetime
    uploaded_df["Send Date"] = pd.to_datetime(uploaded_df["Send Date"], errors="coerce")

    # Show uploaded content for confirmation
    st.write("🧪 Here's what we uploaded:")
    st.dataframe(uploaded_df)

    # Show data types (debug)
    st.write("🔍 Data types:")
    st.write(uploaded_df.dtypes)

    # Store to session
    st.session_state.campaigns = uploaded_df
    st.success("✅ Campaign data uploaded successfully!")

# Initialize empty campaign tracker if nothing uploaded or added yet
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

# Filter and display by date
if not st.session_state.campaigns.empty:
    st.subheader("📆 Filter by Send Date")
    selected_date = st.date_input("Choose a date to view campaigns", value=pd.to_datetime("today"))

    # Make sure 'Send Date' is datetime again (in case it got missed)
    df = st.session_state.campaigns.copy()
    df["Send Date"] = pd.to_datetime(df["Send Date"], errors="coerce")

    # Filter
    filtered_df = df[df["Send Date"] == pd.to_datetime(selected_date)]

    st.subheader("📁 Campaigns on Selected Date")
    st.dataframe(filtered_df)

    if filtered_df.empty:
        st.warning("No campaigns found for that date.")
