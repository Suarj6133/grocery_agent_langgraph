from langchain.tools import tool
import sqlite3

@tool
def calculate_max_revenue(tool_input: str) -> float:
    """
    Calculate revenue by multiplying inventory and unit_price.
    Input format: "inventory,unit_price" (e.g. "374,48")
    Also accepts: "374*48" or "374 48"
    """
    import re
    parts = re.split(r'[,*x\s]+', tool_input.strip())
    
    if len(parts) != 2:
        return f"Error: Expected 'inventory,unit_price' format but got '{tool_input}'"
    
    inventory = int(float(parts[0].strip()))
    unit_price = float(parts[1].strip())
    
    return inventory * unit_price


def get_reorder_data():
    """Returns re-order eligible SKUs as a list of dicts (Inventory/daily_order_qty < 10)."""
    conn = sqlite3.connect("grocery_data.db")
    cursor = conn.execute("""
        SELECT SKU, Inventory, daily_order_qty, 
               ROUND(CAST(Inventory AS FLOAT) / daily_order_qty, 2) as Days_of_Stock
        FROM report 
        WHERE CAST(Inventory AS FLOAT) / daily_order_qty < 10
        ORDER BY Days_of_Stock ASC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [{"SKU": r[0], "Inventory": r[1], "Daily Orders": r[2], "Days of Stock": r[3]} for r in rows]