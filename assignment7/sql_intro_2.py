import sqlite3
import pandas as pd


def create_connection(db_file):
    """Create a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
    return None

def read_data(conn):
    """Read data from SQLite into a Pandas DataFrame."""
    query = """
    SELECT 
        line_items.line_item_id, 
        line_items.quantity, 
        line_items.product_id, 
        products.product_name, 
        products.price
    FROM 
        line_items
    JOIN 
        products ON line_items.product_id = products.product_id
    """
    df = pd.read_sql_query(query, conn)
    return df

def add_total_column(df):
    """Add a 'total' column that calculates the total price per line item."""
    df['total'] = df['quantity'] * df['price']
    return df

def group_and_summarize(df):
    """Group by product_id and calculate the summary (count, sum, first)."""
    summary_df = df.groupby('product_id').agg(
        line_item_count=('line_item_id', 'count'),
        total_price=('total', 'sum'),
        product_name=('product_name', 'first')
    ).reset_index()
    return summary_df


def sort_by_product_name(df):
    """Sort the DataFrame by product_name."""
    sorted_df = df.sort_values(by='product_name')
    return sorted_df

def write_to_csv(df, filename):
    """Write the DataFrame to a CSV file."""
    df.to_csv(filename, index=False)

def main():
    conn = create_connection('../db/lesson.db')
    if not conn:
        return
    
    # 7.2 Read data into a DataFrame
    df = read_data(conn)
    
    # 7.3 Add the 'total' column
    df = add_total_column(df)
    
    # 7.4 Group by product_id and calculate the summary
    summary_df = group_and_summarize(df)
    
    # 7.5 Sort by product_name
    sorted_df = sort_by_product_name(summary_df)
    
    # 7.6 Write the result to a CSV file
    write_to_csv(sorted_df, 'order_summary.csv')
    
    # 7.7 Print the first 5 rows of the resulting DataFrame
    print(sorted_df.head())
    
 
    conn.close()

if __name__ == "__main__":
    main()
