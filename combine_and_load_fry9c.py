import os
import pandas as pd
import sqlite3

# Step 1: Define folders and paths
csv_folder = os.path.join(os.getcwd(), "files")  # folder with CSVs
parquet_path = os.path.join(os.getcwd(), "fry9c_combined.parquet")
sqlite_path = os.path.join(os.getcwd(), "fry9c_data.sqlite")

# Step 2: Combine all CSVs into a single DataFrame
all_data = []

for filename in os.listdir(csv_folder):
    if filename.endswith(".csv"):
        filepath = os.path.join(csv_folder, filename)

        try:
            # Extract metadata from filename
            parts = filename.split("_")
            bank_name = parts[1]
            rssd_id = parts[2]
            report_date = parts[-1].replace(".csv", "")

            df = pd.read_csv(filepath, dtype=str, low_memory=False)
            df["bank_name"] = bank_name
            df["rssd_id"] = rssd_id
            df["report_date"] = report_date

            all_data.append(df)
        except Exception as e:
            print(f"⚠️ Failed to process {filename}: {e}")

# Combine into one DataFrame
combined_df = pd.concat(all_data, ignore_index=True)

# Step 3: Save as Parquet
combined_df.to_parquet(parquet_path, index=False)
print(f"✅ Parquet file created at: {parquet_path}")

# Step 4: Load into SQLite
conn = sqlite3.connect(sqlite_path)
combined_df.to_sql("fry9c_combined", conn, if_exists='replace', index=False)
conn.close()
print(f"✅ Data loaded into SQLite at: {sqlite_path}")
