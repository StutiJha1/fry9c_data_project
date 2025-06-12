import os
import requests
import zipfile
from time import sleep

BASE_URL = "https://www.ffiec.gov/npw/FinancialReport/ReturnBHCFZipFiles?zipfilename="
DOWNLOAD_DIR = "fry9c_data"
CSV_DIR = "fry9c_csv_only"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(CSV_DIR, exist_ok=True)

quarter_end_dates = {
    "03": "0331",
    "06": "0630",
    "09": "0930",
    "12": "1231"
}

years = range(2016, 2025)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Safari/537.36"
}

for year in years:
    for q in ["03", "06", "09", "12"]:
        yyyymmdd = f"{year}{quarter_end_dates[q]}"
        filename = f"BHCF{yyyymmdd}.ZIP"
        url = BASE_URL + filename
        filepath = os.path.join(DOWNLOAD_DIR, filename)

        print(f"Downloading {filename} from {url} ...")
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                with open(filepath, "wb") as f:
                    f.write(response.content)
                print(f"Saved {filename} successfully.")

                # 🧩 Extract only CSV files
                try:
                    with zipfile.ZipFile(filepath, 'r') as zip_ref:
                        for member in zip_ref.namelist():
                            if member.lower().endswith('.csv'):
                                zip_ref.extract(member, path=CSV_DIR)
                                print(f"Extracted CSV: {member}")
                except zipfile.BadZipFile:
                    print(f"Warning: {filename} is not a valid ZIP file.")

            elif response.status_code == 403:
                print(f"Access denied (403) for {filename}. Skipping...")
            elif response.status_code == 404:
                print(f"File not found (404): {filename}. Skipping...")
            else:
                print(f"Failed to download {filename}. HTTP Status: {response.status_code}")
        except Exception as e:
            print(f"Error downloading {filename}: {e}")

        sleep(2)

print("Download and CSV extraction completed.")



