import os
import snowflake.connector

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables from .env
load_dotenv()

# Create our MCP server
mcp = FastMCP("Enterprise Sales Analytics")


def get_snowflake_connection():
    """Create a secure connection to Snowflake."""

    return snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        private_key_file="keys/ai_mcp_service.p8",
        private_key_file_pwd=os.getenv("SNOWFLAKE_PRIVATE_KEY_PASSPHRASE"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        role=os.getenv("SNOWFLAKE_ROLE"),
    )


@mcp.tool()
def get_sales_by_territory() -> list[dict]:
    """
    Retrieve total revenue grouped by sales territory.

    Returns:
        A list containing each territory and its total revenue.
    """

    connection = get_snowflake_connection()

    try:
        cursor = connection.cursor()

        try:
            cursor.execute("""
                SELECT
                    TERRITORY,
                    SUM(REVENUE) AS TOTAL_REVENUE
                FROM ENTERPRISE_AI.SALES.SALES_TRANSACTIONS
                GROUP BY TERRITORY
                ORDER BY TOTAL_REVENUE DESC
            """)

            results = cursor.fetchall()

            return [
                {
                    "territory": territory,
                    "total_revenue": float(revenue),
                }
                for territory, revenue in results
            ]

        finally:
            cursor.close()

    finally:
        connection.close()


if __name__ == "__main__":
    mcp.run(transport="stdio")