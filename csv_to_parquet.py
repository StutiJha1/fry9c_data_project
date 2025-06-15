import os
import pandas as pd
import sqlite3

# Folder where all CSV files are stored
csv_folder = os.path.join(os.getcwd(), "files")
combined_parquet_file = os.path.join(os.getcwd(), "fry9c_combined.parquet")
sqlite_file = os.path.join(os.getcwd(), "fry9c_data.sqlite")

# Step 2: Combine all CSVs into a single DataFrame
all_data = []

for filename in os.listdir(csv_folder):
    if filename.endswith(".csv") and filename.startswith("FRY9C_"):
        filepath = os.path.join(csv_folder, filename)
        try:
            df = pd.read_csv(filepath, encoding='utf-8', low_memory=False)
            df["source_file"] = filename  # Optional: helps trace the origin
            all_data.append(df)
            print(f"✅ Read: {filename}")
        except Exception as e:
            print(f"❌ Failed to read {filename}: {e}")

if not all_data:
    print("❌ No valid CSV files found.")
    exit()

# Step 3: Concatenate all DataFrames
combined_df = pd.concat(all_data, ignore_index=True)
print(f"🔢 Total rows combined: {len(combined_df)}")

# Step 4: Save to Parquet
combined_df.to_parquet(combined_parquet_file, index=False)
print(f"✅ Saved combined data to: {combined_parquet_file}")

# Step 5: Load into SQLite
conn = sqlite3.connect(sqlite_file)
table_name = "fry9c_combined"

# Optional: truncate/replace if table exists
combined_df.to_sql(table_name, conn, if_exists="replace", index=False)
conn.close()
print(f"✅ Loaded into SQLite database: {sqlite_file} (Table: {table_name})")
