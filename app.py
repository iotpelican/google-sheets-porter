import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# 1. Connection Helper
def get_gspread_client():
    creds_info = st.secrets["gcp_service_account"]
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_info, scopes=scopes)
    return gspread.authorize(creds)

st.title("📊 Google Sheets Data Porter")

# Initialize Session State to store our dataframe
if 'processed_df' not in st.session_state:
    st.session_state.processed_df = None

# Sidebar Inputs
with st.sidebar:
    source_id = st.text_input("Source Spreadsheet ID")
    dest_folder_id = st.text_input("Destination Folder ID")
    new_name = st.text_input("New File Name", "Processed_Report")

# STEP 1: PROCESS DATA
if st.button("🚀 1. Process & Preview Data"):
    if not source_id or not dest_folder_id:
        st.error("Please provide both IDs in the sidebar.")
    else:
        try:
            gc = get_gspread_client()
            sh = gc.open_by_key(source_id)
            df = pd.DataFrame(sh.get_worksheet(0).get_all_records())
            
            # Transformation Logic
            df['last_updated'] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Store in session state so it survives the next button click
            st.session_state.processed_df = df
            st.success("Data processed! See preview below.")
        except Exception as e:
            st.error(f"Processing Error: {e}")

# STEP 2: SHOW DOWNLOAD & UPLOAD (Only if data exists)
if st.session_state.processed_df is not None:
    df = st.session_state.processed_df
    st.dataframe(df.head())

    # Local Download Button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Local CSV", data=csv, file_name=f"{new_name}.csv")

    # Upload to Google Drive Button
    if st.button("📤 2. Upload to Google Drive Now"):
        with st.spinner("Uploading to Google Drive..."):
            try:
                gc = get_gspread_client()
                # Create the new sheet in the specific folder
                new_sh = gc.create(new_name, folder_id=dest_folder_id)
                
                # Format data for gspread (headers + values)
                data_to_upload = [df.columns.values.tolist()] + df.values.tolist()
                new_sh.get_worksheet(0).update('A1', data_to_upload)
                
                st.success(f"✅ Successfully uploaded! Link: {new_sh.url}")
                # Clear state after success if desired
                # st.session_state.processed_df = None
            except Exception as e:
                st.error(f"Upload Error: {e}")