import os

# Top 10 US banks and their RSSD IDs (example IDs, replace if needed)
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

# Years to download
years = range(2016, 2025)

# Report type and base URL
report_type = "FRY9C"
base_url = "https://www.ffiec.gov/npw/FinancialReport/ReturnFinancialReportCSV"

# Destination folder
destination_folder = os.getcwd()
os.makedirs(destination_folder, exist_ok=True)

# Loop through each bank and year
for bank_name, rssd_id in banks.items():
    for year in years:
        # Use Q4 date for each year (Dec 31st)
        report_date = f"{year}1231"
        
        url = f"{base_url}?rpt={report_type}&id={rssd_id}&dt={report_date}"
        output_file = f"{report_type}_{bank_name}_{rssd_id}_{report_date}.csv"
        output_path = os.path.join(destination_folder, output_file)

        # Use curl to download the file
        cmd = f'curl --ssl-no-revoke -o "{output_path}" "{url}" ' \
              f'-H "User-Agent: Mozilla/5.0" -H "Referer: https://www.ffiec.gov/npw"'
        
        print(f"Downloading: {output_file}")
        os.system(cmd)




