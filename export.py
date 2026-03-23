import pandas as pd
from database import connect_db

def export_csv():
    conn = connect_db()
    df = pd.read_sql("SELECT * FROM expenses", conn)
    df.to_csv("expenses.csv", index=False)
    conn.close()