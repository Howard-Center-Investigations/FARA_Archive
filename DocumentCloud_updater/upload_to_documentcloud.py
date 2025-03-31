import os
import tempfile
import requests
import pandas as pd
from documentcloud import DocumentCloud
import urllib3

# 🔕 Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 🔐 Get environment variables
username = os.getenv("DOCUMENTCLOUD_USERNAME")
password = os.getenv("DOCUMENTCLOUD_PASSWORD")

if not username or not password:
    raise ValueError("Missing DOCUMENTCLOUD_USERNAME or DOCUMENTCLOUD_PASSWORD in environment variables.")

client = DocumentCloud(username, password)
PROJECT_ID = 221099

# 📂 Resolve path to CSV
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "new_files.csv")

# 📄 Load CSV
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"{csv_path} not found.")

df = pd.read_csv(csv_path)
urls = df["URL"].dropna()

# 🚀 Begin processing
if urls.empty:
    print("📭 No new URLs found in new_files.csv. Nothing to upload.")
else:
    with tempfile.TemporaryDirectory() as temp_dir:
        for url in urls:
            try:
                filename = os.path.basename(url.split("?")[0])
                file_path = os.path.join(temp_dir, filename)

                print(f"⬇️  Downloading: {url}")
                response = requests.get(url, timeout=30, verify=False)
                response.raise_for_status()

                with open(file_path, "wb") as f:
                    f.write(response.content)

                print(f"📤 Uploading: {filename}")
                document = client.documents.upload(
                    file_path,
                    access="public",
                    project=PROJECT_ID
                )

                print(f"✅ Uploaded: {document.title}")
                print(f"🔗 DocumentCloud URL: {document.canonical_url}\n")

            except Exception as e:
                print(f"❌ Failed to process {url}: {e}\n")