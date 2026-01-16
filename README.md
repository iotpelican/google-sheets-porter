# 📊 Google Sheets Data Porter

A Streamlit application to automate data transfer and transformation between Google Drive directories.

## 🚀 Getting Started
1. **Enable APIs:** Ensure Google Drive and Google Sheets APIs are enabled in GCP.
2. **Service Account:** Share your source sheet and destination folder with the service account email.
3. **Secrets:** Add your Service Account JSON to the Streamlit Cloud Secrets dashboard using the `[gcp_service_account]` key.

## 🛠️ Tech Stack
- **Streamlit:** Frontend UI
- **Gspread:** Google Sheets interaction
- **Pandas:** Data manipulation
- **CodeStream:** Team collaboration and code reviews

## 🤝 Collaboration
We use **CodeStream** for in-code discussions. Please refer to the Codemarks in `app.py` for logic explanations.# google-sheets-porter