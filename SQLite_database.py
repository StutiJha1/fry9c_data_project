import os
import sqlite3
import pandas as pd

# Path setup
csv_folder = os.path.join(os.getcwd(), "files")
database_path = os.path.join(os.getcwd(), "fry9c_data.sqlite")

# Connect to (or create) SQLite database
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

# Create table (if not exists)
cursor.execute('DROP TABLE IF EXISTS fry9c_combined')  # Optional: clear old data
conn.commit()

# Read and insert all CSV files
for filename in os.listdir(csv_folder):
    if filename.endswith(".csv"):
        filepath = os.path.join(csv_folder, filename)

        try:
            # Extract bank name from filename (between FRY9C_ and RSSD)
            parts = filename.split("_")
            bank_name = parts[1]  # 'JPMorgan_Chase', 'Bank_of_America', etc.
            report_date = parts[-1].replace(".csv", "")  # e.g., 20181231

            # Read CSV
            df = pd.read_csv(filepath, dtype=str, low_memory=False)

            # Add metadata columns
            df["bank_name"] = bank_name
            df["report_date"] = report_date

            # Insert into database
            df.to_sql("fry9c_combined", conn, if_exists='append', index=False)
            print(f"✅ Loaded: {filename}")
        except Exception as e:
            print(f"⚠️ Skipped: {filename} due to error: {e}")

# Close connection
conn.close()
print("🎉 All files loaded into fry9c_data.sqlite")

