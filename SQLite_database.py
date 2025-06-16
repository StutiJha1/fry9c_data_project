import os
import sqlite3
import pandas as pd

# Set paths
csv_folder = os.path.join(os.getcwd(), "files")
database_path = os.path.join(os.getcwd(), "fry9c_data.sqlite")

# Connect to SQLite
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

# Drop old table if exists
cursor.execute("DROP TABLE IF EXISTS fry9c_combined;")
conn.commit()

# Create new table
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

# Read all CSV files
for filename in os.listdir(csv_folder):
    if filename.endswith(".csv"):
        filepath = os.path.join(csv_folder, filename)
        try:
            parts = filename.replace(".csv", "").split("_")

            # Handle bank names with underscores
            bank_name = "_".join(parts[1:-2])
            rssd_id = parts[-2]
            report_date = parts[-1]

            df = pd.read_csv(filepath, dtype=str, low_memory=False)
            df["bank_name"] = bank_name
            df["rssd_id"] = rssd_id
            df["report_date"] = report_date

            df.to_sql("fry9c_combined", conn, if_exists="append", index=False)
            print(f"✅ Loaded: {filename}")
        except Exception as e:
            print(f"⚠️ Skipped {filename} due to error: {e}")

# Close connection
conn.close()
print("🎉 All files loaded successfully with metadata columns.")




