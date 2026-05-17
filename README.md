# Grocery Agent - LangGraph

An AI-powered grocery inventory assistant built with LangGraph and Groq. It queries a SQLite database and calculates revenue using a custom tool, all orchestrated through a multi-step agent workflow.

## How It Works

The agent follows a graph-based workflow:

```
User Question → Assistant (LLM) → SQL Query → Tools Execute → Assistant → Revenue Calculation → Tools Execute → Final Answer
```

- **Assistant Node**: Calls Groq LLM (llama-3.1-8b-instant) with tool-calling to decide what to do
- **Tools Node**: Executes the requested tool (SQL query or revenue calculation)
- **State**: Maintains the full conversation history as messages flow through the graph

## Project Structure

```
├── agent.py          # LangGraph agent with nodes, edges, and graph compilation
├── custom_tools.py   # Custom calculate_max_revenue tool
├── prompt.py         # System prompt for the LLM
├── user_input.py     # Streamlit frontend
├── load_excel.py     # Script to load grocery_data.xlsx into SQLite
├── grocery_data.db   # SQLite database
├── grocery_data.xlsx # Source Excel data
├── requirements.txt  # Python dependencies
├── .env              # API key (not tracked in git)
└── .gitignore        # Git ignore rules
```

## Setup

1. **Clone the repo**
   ```bash
   git clone <your-repo-url>
   cd grocery_agent_langgraph
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add your Groq API key**

   Create a `.env` file in the project root:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

   Get a free API key from [Groq Console](https://console.groq.com/keys).

4. **Run the Streamlit app**
   ```bash
   streamlit run user_input.py
   ```

## Database Schema

Table: `report`

| Column | Description |
|--------|-------------|
| SKU | Product identifier (e.g. SKU-1, SKU-2) |
| Inventory | Current stock quantity |
| daily_order_qty | Daily order quantity |
| expiry_date | Product expiry date |
| unit_price | Price per unit |
| reorder_time | Reorder lead time in days |
| safety_stock | Safety stock level |

## Custom Tool

**calculate_max_revenue**: Takes `"inventory,unit_price"` as input (e.g. `"374,28"`) and returns `inventory × unit_price`.

The agent is designed to:
1. First query the database for Inventory and unit_price
2. Then pass those values to calculate_max_revenue
3. Report the result to the user

## Tech Stack

- **LangGraph** - Agent orchestration framework
- **Groq** - Fast LLM inference (llama-3.1-8b-instant)
- **LangChain** - SQL toolkit and tool management
- **Streamlit** - Web frontend
- **SQLite** - Database
