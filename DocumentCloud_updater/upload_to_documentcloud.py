import os
import pandas as pd
from documentcloud import DocumentCloud

# Get credentials from environment variables
username = os.getenv("DOCUMENTCLOUD_USERNAME")
password = os.getenv("DOCUMENTCLOUD_PASSWORD")

if not username or not password:
    raise ValueError("Missing DOCUMENTCLOUD_USERNAME or DOCUMENTCLOUD_PASSWORD in environment variables.")

# Initialize DocumentCloud client
client = DocumentCloud(username, password)

# Define the project ID
PROJECT_ID = 221099

# Load new_files.csv
csv_path = "new_files.csv"
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"{csv_path} not found.")

df = pd.read_csv(csv_path)
urls = df["URL"].dropna()

# Check if there are any URLs to upload
if urls.empty:
    print("📭 No new URLs found in new_files.csv. Nothing to upload.")
else:
    for url in urls:
        try:
            print(f"📤 Uploading: {url}")
            document = client.documents.upload(
                url,
                access="public",
                project=PROJECT_ID
            )
            print(f"✅ Uploaded: {document.title}")
            print(f"🔗 DocumentCloud URL: {document.canonical_url}\n")
        except Exception as e:
            print(f"❌ Failed to upload {url}: {e}\n")