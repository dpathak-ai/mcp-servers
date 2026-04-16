## mcp-servers

A small playground repo for building **MCP (Model Context Protocol) servers** with `fastmcp` and connecting to them from an **OpenAI Agents** client over **stdio**.

Included:
- **`mcp_hello.py`**: a simple MCP server exposing greeting/joke/quote/random tools.
- **`mcp_db.py`**: a MySQL MCP server exposing a **read-only** `run_query` tool (SELECT/WITH/EXPLAIN only).
- **`main.py`**: an Agents client that spawns an MCP server via `uv run ...` and calls it through `MCPServerStdio`.

## Requirements

- Python (see `pyproject.toml` for the configured version)
- [`uv`](https://github.com/astral-sh/uv)

## Setup

```bash
uv sync
```

If you use a `.env`, it will be loaded by the scripts (via `python-dotenv`).

## Run

### Start the hello MCP server

```bash
uv run mcp_hello.py
```

### Start the MySQL MCP server

```bash
uv run mcp_db.py
```

Environment variables used by `mcp_db.py`:
- `MYSQL_HOST` (default: `localhost`)
- `MYSQL_PORT` (default: `3306`)
- `MYSQL_USER` (required)
- `MYSQL_PASSWORD` (required)
- `MYSQL_DATABASE` (optional, depending on your queries)

### Run the Agents client (stdio MCP)

`main.py` spawns the MCP server as a subprocess (currently `mcp_hello.py`) and connects over stdio:

```bash
uv run main.py
```

