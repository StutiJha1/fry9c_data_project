# Step 1–2: Import libraries and connect to database
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Replace this path with the actual path to your SQLite database file
conn = sqlite3.connect('/Users/stutijha/Desktop/FRY9C_DATA_PROJECT/fry9c_data.sqlite')

# Step 3: Query to compare one item across all banks for a specific date
query1 = """
SELECT 
    bank_name,
    rssd_id,
    report_date,
    CAST(Value AS REAL) AS total_assets
FROM fry9c_combined
WHERE ItemName = 'BHCK0081'
  AND report_date = '20240930'
ORDER BY total_assets DESC;
"""
df1 = pd.read_sql_query(query1, conn)

# Step 4: Query to compare one item across time for one bank
query2 = """
SELECT 
    report_date,
    bank_name,
    CAST(Value AS REAL) AS value_numeric
FROM fry9c_combined
WHERE ItemName = 'BHCK2170'
  AND bank_name = 'JPMorgan_Chase'
ORDER BY report_date;
"""
df2 = pd.read_sql_query(query2, conn)

# Step 5: Plot bar chart for total assets by bank
plt.figure(figsize=(12, 6))
plt.bar(df1['bank_name'], df1['total_assets'], color='skyblue')
plt.xticks(rotation=90)
plt.title("Total Assets by Bank (BHCK0081) on 20240930")
plt.ylabel("Total Assets")
plt.tight_layout()
plt.show()

# Step 6: Plot line chart of BHCK2170 for JPMorgan over time
df2['report_date'] = pd.to_datetime(df2['report_date'])

plt.figure(figsize=(10, 5))
plt.plot(df2['report_date'], df2['value_numeric'], marker='o', linestyle='-')
plt.title("Trend of BHCK2170 for JPMorgan_Chase Over Time")
plt.xlabel("Report Date")
plt.ylabel("Value")
plt.grid(True)
plt.tight_layout()
plt.show()


