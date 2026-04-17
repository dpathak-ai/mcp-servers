import os
from typing import Any, Dict, List, Optional

import anyio
from dotenv import load_dotenv
from fastmcp import FastMCP


# Load DB credentials (and other local config) from a `.env` file if present.
load_dotenv()

# MCP server exposing a small, safety-focused MySQL query surface.
mcp = FastMCP("mysql-mcp")


def _get_mysql_config() -> Dict[str, Any]:
    """Read MySQL configuration from environment variables."""
    host = os.getenv("MYSQL_HOST", "localhost")
    port = int(os.getenv("MYSQL_PORT", "3306"))
    user = os.getenv("MYSQL_USER")
    password = os.getenv("MYSQL_PASSWORD")
    database = os.getenv("MYSQL_DATABASE")

    if not user or not password:
        raise RuntimeError("MYSQL_USER and MYSQL_PASSWORD must be set in the environment.")

    return {
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "database": database,
    }


def _ensure_read_only(sql: str) -> None:
    """Basic safety check to ensure query is read-only."""
    normalized = sql.strip().lower()

    # allow CTEs (WITH ...) and simple SELECT/EXPLAIN
    allowed_starts = ("select", "with", "explain")
    if not normalized.startswith(allowed_starts):
        raise ValueError("Only read-only queries (SELECT/WITH/EXPLAIN) are allowed.")

    forbidden = ("insert ", "update ", "delete ", "drop ", "alter ", "truncate ", "create ")
    if any(keyword in normalized for keyword in forbidden):
        raise ValueError("Mutating queries are not allowed.")


async def _run_mysql_query(sql: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Execute a read-only query against MySQL and return rows as list of dicts.

    Uses a synchronous driver under the hood via a worker thread to keep the
    MCP event loop responsive.
    """
    import mysql.connector  # imported here so the module isn't required unless used

    config = _get_mysql_config()

    def _sync_query() -> List[Dict[str, Any]]:
        # mysql-connector-python is synchronous; run it off the event loop to avoid
        # blocking other MCP requests.
        conn = mysql.connector.connect(**config)
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, params or {})
            rows = cursor.fetchall()
            # MCP responses are JSON-encoded; coerce common DB-native types.
            result: List[Dict[str, Any]] = []
            for row in rows:
                cleaned: Dict[str, Any] = {}
                for k, v in row.items():
                    if hasattr(v, "isoformat"):
                        cleaned[k] = v.isoformat()
                    else:
                        cleaned[k] = v
                result.append(cleaned)
            return result
        finally:
            conn.close()

    return await anyio.to_thread.run_sync(_sync_query)


@mcp.tool()
async def run_query(sql: str, params: Optional[Dict[str, Any]] = None) -> list[dict]:
    """
    MCP tool: execute a read-only MySQL query and return the result rows.

    This is designed to be exposed as a command in the OpenAI Agents framework.
    """
    _ensure_read_only(sql)
    rows = await _run_mysql_query(sql, params)
    return rows


if __name__ == "__main__":
    # Default is stdio transport, ideal for OpenAI Agents / MCP clients.
    mcp.run()
