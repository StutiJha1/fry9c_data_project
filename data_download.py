import os

# Top US banks and RSSD IDs
banks = {
    'JPMorgan_Chase': '1073757',
    'Bank_of_America': '1073756',
    'Citigroup': '1039502',
    'Wells_Fargo': '1120754',
    'U.S._Bancorp': '1119794',
    'PNC': '1069778',
    'Truist': '4855594',
    'Goldman_Sachs': '2380443',
    'Morgan_Stanley': '2162966',
    'Capital_One': '1038207'
}

years = range(2016, 2025)
quarters = ['0331', '0630', '0930', '1231']  # Q1 to Q4
report_type = "FRY9C"
base_url = "https://www.ffiec.gov/npw/FinancialReport/ReturnFinancialReportCSV"
destination_folder = os.getcwd()
os.makedirs(destination_folder, exist_ok=True)

for bank_name, rssd_id in banks.items():
    for year in years:
        for quarter in quarters:
            report_date = f"{year}{quarter}"
            url = f"{base_url}?rpt={report_type}&id={rssd_id}&dt={report_date}"
            output_file = f"{report_type}_{bank_name}_{rssd_id}_{report_date}.csv"
            output_path = os.path.join(destination_folder, output_file)

            # Use curl with -L and browser headers
            cmd = (
                f'curl -L --ssl-no-revoke -o "{output_path}" "{url}" '
                f'-H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                f'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36" '
                f'-H "Referer: https://www.ffiec.gov/npw" '
                f'-H "Accept: text/csv,application/csv;q=0.9,*/*;q=0.8"'
            )

            print(f"Downloading: {output_file}")
            os.system(cmd)

            # Check if file is a valid CSV or an HTML error page
            try:
                with open(output_path, 'r', encoding='utf-8', errors='ignore') as f:
                    first_line = f.readline()
                    if first_line.startswith("<!DOCTYPE html>") or "<html" in first_line.lower():
                        print(f"⚠️  Invalid file (HTML received): {output_file}")
                        os.remove(output_path)
                    else:
                        print(f"✅  Successfully downloaded: {output_file}")
            except FileNotFoundError:
                print(f"❌  File not found after download attempt: {output_file}")

