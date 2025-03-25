import os
import requests
import zipfile
from io import BytesIO
import urllib3

# Disable insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Define the target directory for downloads
DOWNLOAD_DIR = os.path.dirname(os.path.abspath(__file__))

# List of FARA bulk data URLs
urls = [
    "https://efile.fara.gov/bulk/zip/FARA_All_Registrants.csv.zip?1742919005845.6677",
    "https://efile.fara.gov/bulk/zip/FARA_All_RegistrantDocs.csv.zip?1742919005845.6677",
    "https://efile.fara.gov/bulk/zip/FARA_All_ShortForms.csv.zip?1742919005845.6677",
    "https://efile.fara.gov/bulk/zip/FARA_All_ForeignPrincipals.csv.zip?1742919005845.6677",
]

def download_and_extract_zip(url, dest_folder):
    filename = url.split("/")[-1].split("?")[0]
    print(f"Downloading: {filename}")

    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()

        with zipfile.ZipFile(BytesIO(response.content)) as z:
            z.extractall(dest_folder)
            print(f"Extracted: {filename} → {dest_folder}")
    except Exception as e:
        print(f"Failed to download or extract {filename}: {e}")

def main():
    for url in urls:
        download_and_extract_zip(url, DOWNLOAD_DIR)

if __name__ == "__main__":
    main()