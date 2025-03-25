# list_comparison.py

import requests
import zipfile
import io
import os
import urllib3
import pandas as pd

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def download_and_extract_zip(url, extract_to_folder="current_list"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    extract_to = os.path.join(script_dir, extract_to_folder)

    os.makedirs(extract_to, exist_ok=True)

    print(f"Downloading from {url} (SSL verify disabled)...")
    response = requests.get(url, verify=False)
    response.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        z.extractall(extract_to)
        print(f"Extracted files to '{extract_to}': {z.namelist()}")

def find_csv_in_folder(folder_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(script_dir, folder_name)

    csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {folder_path}")

    return os.path.join(folder_path, csv_files[0])

def compare_url_columns(current_csv, prior_csv, output_csv):
    current_df = pd.read_csv(current_csv, usecols=["URL"], encoding="ISO-8859-1")
    prior_df = pd.read_csv(prior_csv, usecols=["URL"], encoding="ISO-8859-1")

    current_urls = set(current_df["URL"].dropna())
    prior_urls = set(prior_df["URL"].dropna())

    new_urls = current_urls - prior_urls

    new_df = pd.DataFrame(sorted(new_urls), columns=["URL"])
    new_df.to_csv(output_csv, index=False)
    print(f"New URLs saved to {output_csv}")

if __name__ == "__main__":
    ZIP_URL = "https://efile.fara.gov/bulk/zip/FARA_All_RegistrantDocs.csv.zip?1742933813017.4006"
    download_and_extract_zip(ZIP_URL)

    current_csv_path = find_csv_in_folder("current_list")
    prior_csv_path = find_csv_in_folder("prior_list")
    output_csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "new_files.csv")

    compare_url_columns(current_csv_path, prior_csv_path, output_csv_path)
