import os
import requests
from time import sleep

BASE_URL = "https://www.ffiec.gov/npw/FinancialReport/ReturnBHCFZipFiles?zipfilename="
DOWNLOAD_DIR = "fry9c_data"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

quarter_end_dates = {
    "03": "0331",
    "06": "0630",
    "09": "0930",
    "12": "1231"
}

years = range(2016, 2025)

for year in years:
    for q in ["03", "06", "09", "12"]:
        yyyymmdd = f"{year}{quarter_end_dates[q]}"
        filename = f"BHCF{yyyymmdd}.ZIP"
        url = BASE_URL + filename
        filepath = os.path.join(DOWNLOAD_DIR, filename)

        print(f"Downloading {filename} from {url} ...")
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(filepath, "wb") as f:
                    f.write(response.content)
                print(f"Saved {filename} successfully.")
            else:
                print(f"Failed to download {filename}. HTTP Status: {response.status_code}")
        except Exception as e:
            print(f"Error downloading {filename}: {e}")

        sleep(1)

print("Download attempts completed.")


