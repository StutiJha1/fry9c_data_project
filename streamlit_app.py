# streamlit_app.py

import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Connect to database
conn = sqlite3.connect('/Users/stutijha/Desktop/FRY9C_DATA_PROJECT/fry9c_data.sqlite')

st.title("FR Y-9C Bank Data Explorer")

# Load list of unique banks, dates, and rssd_ids for dropdowns
bank_list = pd.read_sql_query("SELECT DISTINCT bank_name FROM fry9c_combined ORDER BY bank_name;", conn)
date_list = pd.read_sql_query("SELECT DISTINCT report_date FROM fry9c_combined ORDER BY report_date DESC;", conn)
rssd_list = pd.read_sql_query("SELECT DISTINCT rssd_id FROM fry9c_combined ORDER BY rssd_id;", conn)

# User inputs
selected_bank = st.selectbox("Select Bank Name", bank_list['bank_name'])
selected_date = st.selectbox("Select Report Date", date_list['report_date'])
selected_rssd = st.selectbox("Select RSSD ID", rssd_list['rssd_id'])

# Query 1: Total assets on selected date for all banks
query1 = f"""
SELECT bank_name, rssd_id, CAST(Value AS REAL) AS total_assets
FROM fry9c_combined
WHERE ItemName = 'BHCK0081' AND report_date = '{selected_date}'
ORDER BY total_assets DESC;
"""
df1 = pd.read_sql_query(query1, conn)

# Query 2: BHCK2170 trend for selected bank
query2 = f"""
SELECT report_date, CAST(Value AS REAL) AS value_numeric
FROM fry9c_combined
WHERE ItemName = 'BHCK2170' AND bank_name = '{selected_bank}'
ORDER BY report_date;
"""
df2 = pd.read_sql_query(query2, conn)
df2['report_date'] = pd.to_datetime(df2['report_date'])

# Query 3: Scatterplot data for selected date
query3 = f"""
SELECT bank_name, rssd_id, ItemName, CAST(REPLACE(Value, ',', '') AS REAL) AS value
FROM fry9c_combined
WHERE report_date = '{selected_date}' AND ItemName IN ('BHCK0081', 'BHCK2170');
"""
df_raw = pd.read_sql_query(query3, conn)
df_pivot = df_raw.pivot_table(index=['bank_name', 'rssd_id'], columns='ItemName', values='value').reset_index()
df_pivot = df_pivot.rename(columns={'BHCK0081': 'total_assets', 'BHCK2170': 'total_deposits'}).dropna()

# Charts
st.subheader("Total Assets on Selected Date")
st.bar_chart(df1.set_index('bank_name')['total_assets'])

st.subheader(f"Trend of BHCK2170 Over Time for {selected_bank}")
fig1, ax1 = plt.subplots()
ax1.plot(df2['report_date'], df2['value_numeric'], marker='o')
ax1.set_xlabel("Report Date")
ax1.set_ylabel("Value")
ax1.set_title("BHCK2170 Over Time")
st.pyplot(fig1)

st.subheader("Scatterplot: Total Assets vs Total Deposits")
fig2, ax2 = plt.subplots()
ax2.scatter(df_pivot['total_assets'], df_pivot['total_deposits'], alpha=0.6, color='purple')
ax2.set_xlabel("Total Assets")
ax2.set_ylabel("Total Deposits")
ax2.set_title("Scatterplot on " + selected_date)
st.pyplot(fig2)
