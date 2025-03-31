import os
import pandas as pd
from documentcloud import DocumentCloud

# Get environment variables
username = os.getenv("DOCUMENTCLOUD_USERNAME")
password = os.getenv("DOCUMENTCLOUD_PASSWORD")

if not username or not password:
    raise ValueError("Missing DOCUMENTCLOUD_USERNAME or DOCUMENTCLOUD_PASSWORD in environment variables.")

client = DocumentCloud(username, password)
PROJECT_ID = 221099

# Use absolute path based on script location
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "new_files.csv")

# Load CSV
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"{csv_path} not found.")

df = pd.read_csv(csv_path)
urls = df["URL"].dropna()

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