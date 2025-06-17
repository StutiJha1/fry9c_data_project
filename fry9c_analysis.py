# Step 1: Import libraries and connect to database
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


conn = sqlite3.connect('/Users/stutijha/Desktop/FRY9C_DATA_PROJECT/fry9c_data.sqlite')

# Step 2: Query1 to compare one item across all banks for a specific date
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

# Step 3: Query2 to compare one item across time for one bank
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


# Step 4: Query3 both total assets and deposits for the same date
query3 = """
SELECT 
    bank_name,
    rssd_id,
    report_date,
    ItemName,
    CAST(REPLACE(Value, ',', '') AS REAL) AS value
FROM fry9c_combined
WHERE report_date = '20240930'
  AND ItemName IN ('BHCK0081', 'BHCK2170');
"""

df_scatter_raw = pd.read_sql_query(query3, conn)

# Step 5: Pivot the data to get one row per bank with both values
df_scatter = df_scatter_raw.pivot_table(
    index=['bank_name', 'rssd_id', 'report_date'],
    columns='ItemName',
    values='value'
).reset_index()

# Rename columns for clarity
df_scatter = df_scatter.rename(columns={
    'BHCK0081': 'total_assets',
    'BHCK2170': 'total_deposits'
})

# Step 6: Drop rows with missing values
df_scatter = df_scatter.dropna()

# Step 7: for Q3 Plot scatterplot
# relationship between total assets and total deposits across banks on 20240930 using a scatterplot.
plt.figure(figsize=(10, 6))
plt.scatter(df_scatter['total_assets'], df_scatter['total_deposits'], alpha=0.6, color='purple')
plt.xlabel("Total Assets")
plt.ylabel("Total Deposits")
plt.title("Scatterplot: Total Assets vs Total Deposits (20240930)")
plt.grid(True)
plt.tight_layout()
plt.show()

# Step 8: for Q1 Plot bar chart for total assets by bank
#total assets (BHCK0081) for all banks on 20240930 using a bar chart.
plt.figure(figsize=(12, 6))
plt.bar(df1['bank_name'], df1['total_assets'], color='skyblue')
plt.xticks(rotation=90)
plt.title("Total Assets by Bank (BHCK0081) on 20240930")
plt.ylabel("Total Assets")
plt.tight_layout()
plt.show()

# Step 9: for Q2 Plot line chart of BHCK2170 for JPMorgan over time
# a line chart on how BHCK2170 changes over time for JPMorgan_Chase
df2['report_date'] = pd.to_datetime(df2['report_date'])

plt.figure(figsize=(10, 5))
plt.plot(df2['report_date'], df2['value_numeric'], marker='o', linestyle='-')
plt.title("Trend of BHCK2170 for JPMorgan_Chase Over Time")
plt.xlabel("Report Date")
plt.ylabel("Value")
plt.grid(True)
plt.tight_layout()
plt.show()


