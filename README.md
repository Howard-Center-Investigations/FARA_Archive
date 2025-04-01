# FARA Archive

This is an archive of Foreign Agent Registration Act filings and data.

### FARA Filings PDFs

[This link](https://www.documentcloud.org/projects/221099-fara-storage-public/) goes to an archive on DocumentCloud that hosts all FARA filings, of every type, dating back to the very first filing in 1942.

- The file [FARA_All_RegistrantDocs.csv](https://github.com/Howard-Center-Investigations/FARA_Archive/raw/refs/heads/main/bulk_data_files/FARA_All_RegistrantDocs.csv) in this repository contains a column "URL" which can be used to search the DocumentCloud archive for individual filings. The names of files in DocumentCloud are derived from the end of the urls that (currently) lead to the DOJ's copy of the record. So if you want to search DocumentCloud for a file whose url is "https://efile.fara.gov/docs/7002-Informational-Materials-20250328-379.pdf" then search DocumentCloud for "7002-Informational-Materials-20250328-379".

- The DocumentCloud archive is automatically updated a minimum of once per day. The DOJ often releases new filings from recent days in batches, meaning there are often filings that are date stamped for a particular day but won't actually appear in the DOJ's data (or our DocumentCloud archive) until several days later.

- Big chunks of Short Forms and Registration Statements from 1942-2008 aren't available on the DOJ's website and are instead listed as "Available-FARA-Public-Office" in the excel doc, and therefore aren't included in our archive

- The file failed_fara_downloads.csv in the repository contains a list of filings that cannot be successfully downloaded using the urls provided at FARA.gov

- As of 4/1/2025 the archive consists of over 118,000 documents. There appear to be at least two missing -- I'll work to identify which those are and why they didn't upload

### "Browse Filings" Datasets

The "datasets" folder in this repository contains datasets from the [Browse Filings](https://efile.fara.gov/ords/fara/f?p=1381:1:1551967097995:::::) page of FARA.gov.

- These files are updated a minimum of once per day

### "Bulk Data" csvs

The "bulk_data_files folder" in this repository contains the csv files available for download from the [Bulk Data](https://efile.fara.gov/ords/fara/f?p=107:21::::::) page of FARA/gov.

- These files are updated a minimum of once per day
