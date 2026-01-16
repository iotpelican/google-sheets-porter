import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from io import BytesIO

# 1. Secure Connection using Streamlit Secrets
def get_gspread_client():
    creds_info = st.secrets["gcp_service_account"]
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_info(creds_info, scopes=scopes)
    client = gspread.authorize(creds)
    return client

st.set_page_config(page_title="Data Porter Pro", layout="wide")
st.title("📊 Google Sheets Data Porter & Archiver")

# Sidebar for configuration
with st.sidebar:
    st.header("Step 1: Configuration")
    source_id = st.text_input("Source Spreadsheet ID")
    dest_folder_id = st.text_input("Destination Folder ID")
    new_name = st.text_input("New File Name", "Processed_Report")

if st.button("🚀 Process Data"):
    if not source_id or not dest_folder_id:
        st.warning("Please provide both Source and Destination IDs.")
    else:
        try:
            gc = get_gspread_client()
            
            # --- PHASE 1: EXTRACT ---
            st.info("🔍 Fetching source data...")
            sh = gc.open_by_key(source_id)
            df = pd.DataFrame(sh.get_worksheet(0).get_all_records())

            # --- PHASE 2: TRANSFORM ---
            st.info("🛠️ Transforming data...")
            df['last_updated'] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            # You can add more column logic here!

            # --- PHASE 3: LOCAL DOWNLOAD ---
            st.subheader("✅ Data Processed Successfully")
            
            # Create a CSV buffer for download
            csv_data = df.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="📥 Download as CSV (Local Backup)",
                data=csv_data,
                file_name=f"{new_name}.csv",
                mime="text/csv",
            )
            
            st.dataframe(df.head(10))

            # --- PHASE 4: LOAD TO GOOGLE DRIVE ---
            if st.button("Confirm: Upload to Google Drive"):
                st.write("📁 Creating new file in destination...")
                new_sh = gc.create(new_name, folder_id=dest_folder_id)
                
                # Upload Data
                data_to_upload = [df.columns.values.tolist()] + df.values.tolist()
                new_sh.get_worksheet(0).update('A1', data_to_upload)

                st.success(f"Done! New sheet created: {new_sh.url}")

        except Exception as e:
            st.error(f"Error: {e}")