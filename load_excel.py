import pandas as pd
import sqlite3

DB_PATH = "grocery_data.db"

def load_excel_to_sqlite():
    conn = sqlite3.connect(DB_PATH)
    df1 = pd.read_excel("grocery_data.xlsx")
    df1.to_sql("report", conn, if_exists="replace", index=False)

    conn.close()
    print("excel file uploaded")


if __name__ == "__main__":
    load_excel_to_sqlite()

