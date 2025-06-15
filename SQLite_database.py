import os
import sqlite3
import pandas as pd

csv_folder = os.path.join(os.getcwd(), "files")
database_path = os.path.join(os.getcwd(), "fry9c_data.sqlite")

conn = sqlite3.connect(database_path)
cursor = conn.cursor()

# Drop old table if it exists
cursor.execute("DROP TABLE IF EXISTS fry9c_combined;")
conn.commit()

# You can create the table explicitly if you want control over schema
cursor.execute("""
CREATE TABLE fry9c_combined (
    bank_name TEXT,
    rssd_id TEXT,
    report_date TEXT,
    ItemName TEXT,
    Description TEXT,
    Value TEXT
);
""")
conn.commit()

for filename in os.listdir(csv_folder):
    if filename.endswith(".csv"):
        filepath = os.path.join(csv_folder, filename)

        # Example filename: FRY9C_JPMorgan_Chase_123456_20160331.csv
        # Adjust this extraction to match your real filenames
        parts = filename.replace(".csv", "").split("_")

        try:
            bank_name = parts[1]  # Assuming 2nd part is bank name
            rssd_id = parts[2]    # Assuming 3rd part is rssd_id
            report_date = parts[3] # Assuming 4th part is report date

            df = pd.read_csv(filepath, dtype=str, low_memory=False)

            # Add metadata columns
            df["bank_name"] = bank_name
            df["rssd_id"] = rssd_id
            df["report_date"] = report_date

            # Insert into DB
            df.to_sql("fry9c_combined", conn, if_exists="append", index=False)
            print(f"Loaded: {filename}")
        except Exception as e:
            print(f"Skipped {filename} due to error: {e}")

conn.close()
print("All files loaded with bank_name, rssd_id, and report_date columns.")


