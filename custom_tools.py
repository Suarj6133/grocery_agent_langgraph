from langchain.tools import tool

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