# NEXUS Agentic AI — Retail Analytics Platform

A multi-agent AI system built with **Google ADK** and **Gemini 2.5 Flash** that provides intelligent analytics, data engineering, and business insights for a retail e-commerce company. Specialized agents communicate via **MCP (Model Context Protocol)** servers to handle authentication, database operations, visualization, analysis, web research, and file parsing.

---

## Architecture

```
User
 └── Coordinator Agent (Orchestrator)
       ├── Authenticator Agent      → MySQL login gate
       ├── Data Engineer Agent  ──► Data Engineer MCP (Port 8001)
       │                                ├── describe_database
       │                                ├── fetch_data (SELECT)
       │                                ├── modify_data (INSERT/UPDATE/DELETE)
       │                                └── manage_schema (CREATE/ALTER)
       ├── Visualization Agent  ──► Analytics MCP (Port 8002)
       │                                └── create_chart (bar/line/pie/scatter/heatmap)
       ├── Analysis Agent           → LLM-based business insights
       ├── File Reader Agent        → CSV / Excel ingestion (GUI file picker)
       └── Web Research Agent       → Google Search (real-time market data)
```

### Flow

1. **Auth Gate** — every session starts by verifying the user against the `users` table. Role (`admin` / `employee`) is stored in session state.
2. **Fetch-then-Delegate** — the Coordinator fetches data from the Data Engineer MCP and injects it directly into the next specialist's prompt before delegation.
3. **RBAC** — employees can only read; admins can modify data with a mandatory double-confirmation step before any destructive SQL runs.

---

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | 3.10+ |
| MySQL | 5.7+ / 8.0+ |
| Google API Key | Gemini 2.5 Flash access |

---

## Setup

### 1. Clone and install dependencies

```bash
git clone <repo-url>
cd "main codes"
pip install -r requirements.txt
```

### 2. Configure environment variables

Copy the example file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env`:

```env
GOOGLE_API_KEY=your_google_api_key_here
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=ecommerce_db
```

Also create `main_agent/.env` with at minimum:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

### 3. Set up the database

Import the schema and seed data into MySQL:

```bash
mysql -u root -p < db_file.sql
```

This creates the `ecommerce_db` database with 8 tables and sample data including two users:

| Username | Role |
|----------|------|
| Varun Manager | admin |
| Rahul Staff | employee |

---

## Running the System

The system has three components that must all be running simultaneously.

### Terminal 1 — Data Engineer MCP Server

```bash
cd mcp_servers/data_engineer_mcp
python mcp_server.py
# Listening on http://localhost:8001/mcp
```

### Terminal 2 — Analytics MCP Server

```bash
cd mcp_servers/analysis_mcp
python mcp_server.py
# Listening on http://localhost:8002/mcp
# Charts served at http://localhost:8002/plots/
```

### Terminal 3 — ADK Agent

```bash
cd main_agent
adk web
# Opens the ADK web UI, typically at http://localhost:8000
```

---

## Features

### Authentication
- Username lookup against MySQL `users` table
- Role stored in session state; no further access until auth succeeds

### Data Engineering (RBAC)
- **Employees**: read-only access (`describe_database`, `fetch_data`)
- **Admins**: full access with a mandatory confirmation prompt before any `modify_data` or `manage_schema` call
- Schema introspection via `information_schema`

### Visualization
Supports five chart types rendered with matplotlib/seaborn and saved as PNG:

| Chart | Use case |
|-------|----------|
| `bar` | Comparing categories (sales by product) |
| `line` | Trends over time (monthly revenue) |
| `pie` | Proportional breakdown (market share) |
| `scatter` | Two-variable relationships |
| `heatmap` | Cross-tabulated values |

Charts are saved to `generated_plots/` and served statically at `http://localhost:8002/plots/`.

### Business Analysis
LLM-powered analysis using data injected by the Coordinator:
- Revenue and margin predictions
- Return/refund risk identification
- Strategic recommendations based on retail domain knowledge

### File Reading
- GUI file picker (tkinter) for browsing local CSV and Excel files
- Reads first 500 rows to stay within LLM context limits
- Supports `.csv`, `.xlsx`, `.xls`

### Web Research
- Real-time Google Search via ADK's built-in `google_search` tool
- Used for competitor pricing, market trends, and external benchmarks
- Can be combined with internal data for hybrid analysis

---

## Database Schema

```
users           → user_id, name, email, role (admin/employee)
customers       → customer_id, name, city, country
products        → product_id, name, category, price, cost_price
orders          → order_id, customer_id, order_date, total_amount, status
order_items     → order_item_id, order_id, product_id, quantity, price_at_purchase
payments        → payment_id, order_id, payment_method, payment_status, amount
returns         → return_id, order_item_id, reason, refund_amount
```

---

## Project Structure

```
main codes/
├── main_agent/
│   ├── .env                        # API keys (not committed)
│   ├── coordinator_agent/agent.py  # Orchestrator — root_agent entry point
│   ├── authenticator_agent/agent.py
│   ├── data_engineer_agent/agent.py
│   ├── visualization_agent/agent.py
│   ├── analysis_agent/agent.py
│   ├── file_reader_agent/agent.py
│   └── web_search_agent/agent.py
├── mcp_servers/
│   ├── data_engineer_mcp/
│   │   ├── mcp_server.py           # FastMCP server on port 8001
│   │   └── tools.py                # MySQL query helpers
│   └── analysis_mcp/
│       ├── mcp_server.py           # FastMCP server on port 8002
│       └── tools/
│           └── viz_tools.py        # matplotlib/seaborn chart generation
├── generated_plots/                # Chart output directory (auto-created)
├── db_file.sql                     # Database schema + seed data
├── csv_data.csv                    # Sample CSV for file reader testing
├── excel_data.xlsx                 # Sample Excel for file reader testing
├── .env.example                    # Environment variable template
├── requirements.txt
└── README.md
```

---

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `GOOGLE_API_KEY` | — | Gemini API key (required) |
| `DB_HOST` | `localhost` | MySQL server host |
| `DB_USER` | `root` | MySQL username |
| `DB_PASSWORD` | — | MySQL password (required) |
| `DB_NAME` | `ecommerce_db` | Target database name |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Agent Framework | Google ADK |
| LLM | Gemini 2.5 Flash |
| MCP Framework | FastMCP + Starlette |
| Database | MySQL |
| Data Processing | pandas |
| Visualization | matplotlib, seaborn |
| File Picking | tkinter |
| Web Search | Google Search (ADK built-in) |
| HTTP Server | uvicorn |
