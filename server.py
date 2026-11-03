import os
import snowflake.connector
from pathlib import Path
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
import salesforce

# Load environment variables from .env
PROJECT_DIR = Path(__file__).resolve().parent

load_dotenv(PROJECT_DIR / ".env")

# Create our MCP server
mcp = FastMCP("Enterprise Sales Analytics")


def get_snowflake_connection():
    """Create a secure connection to Snowflake."""

    return snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        private_key_file=str(PROJECT_DIR / "keys" / "ai_mcp_service.p8"),
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
        
        
@mcp.tool()
def get_sales_by_representative() -> list[dict]:
        """Retrieve total revenue grouped by sales representative.
        Returns:
        A list containing sales reps and their total revenue.
        """
    
        connection = get_snowflake_connection()
    
        try:
            cursor = connection.cursor()
    
            try:
                cursor.execute("""
                    SELECT
                        SALES_REP,
                        SUM(REVENUE) AS TOTAL_REVENUE
                    FROM ENTERPRISE_AI.SALES.SALES_TRANSACTIONS
                    GROUP BY SALES_REP
                    ORDER BY TOTAL_REVENUE DESC;
                """)
    
                results = cursor.fetchall()
    
                return [
                    {
                        "sales_Rep": sales_rep,
                        "total_revenue": float(rep_revenue),
                    }
                    for sales_rep, rep_revenue in results
                ]
    
            finally:
                cursor.close()
    
        finally:
            connection.close()
            
            
@mcp.tool()
def get_crm_accounts() -> list[dict]:
    """
    Retrieve Salesforce CRM accounts.

    Returns account names, industries, and billing locations.
    """
    return salesforce.get_salesforce_accounts()
            
    

if __name__ == "__main__":
    mcp.run(transport="stdio")