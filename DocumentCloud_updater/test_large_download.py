import os
import requests
from documentcloud import DocumentCloud

# Get credentials from environment variables
DC_USERNAME = os.environ.get("DOCUMENTCLOUD_USERNAME")
DC_PASSWORD = os.environ.get("DOCUMENTCLOUD_PASSWORD")

# URL of the PDF
url = "https://efile.fara.gov/docs/7009-Supplemental-Statement-20241031-8.pdf"

# Local filename to save the PDF
filename = "7009-Supplemental-Statement.pdf"

# Send HTTP GET request to the URL with SSL verification disabled
try:
    response = requests.get(url, verify=False)
    
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"PDF downloaded successfully as '{filename}'")
        
        # Upload the file to DocumentCloud
        client = DocumentCloud(DC_USERNAME, DC_PASSWORD)

        print("Uploading PDF to DocumentCloud...")
        doc = client.documents.upload(
            filename,
            project=221099,
            access="public"
        )
        print(f"Upload complete: {doc.canonical_url}")

    else:
        print(f"Failed to download PDF. Status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred during download: {e}")

except Exception as e:
    print(f"An error occurred during upload: {e}")
