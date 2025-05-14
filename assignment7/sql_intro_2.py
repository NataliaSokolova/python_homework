import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('../db/lesson.db')

# Define the SQL query
query = '''
SELECT
    line_items.line_item_id,
    line_items.quantity,
    line_items.product_id,
    products.product_name,
    products.price
FROM
    line_items
JOIN
    products
ON
    line_items.product_id = products.product_id
'''

# Load the data into a DataFrame
df = pd.read_sql_query(query, conn)

# Print first 5 rows
print("Initial join result:")
print(df.head())

# Add total column
df['total'] = df['quantity'] * df['price']

# Print first 5 rows with total
print("\nData with total column:")
print(df.head())

# Group by product_id and aggregate
summary_df = df.groupby('product_id').agg({
    'line_item_id': 'count',
    'total': 'sum',
    'product_name': 'first'
}).reset_index()

# Rename columns for clarity
summary_df.rename(columns={
    'line_item_id': 'order_count',
    'total': 'total_price'
}, inplace=True)

# Sort by product_name
summary_df.sort_values('product_name', inplace=True)

# Print the summary
print("\nGrouped and sorted summary:")
print(summary_df.head())

# Write to CSV
summary_df.to_csv('order_summary.csv', index=False)

# Close the connection
conn.close()
