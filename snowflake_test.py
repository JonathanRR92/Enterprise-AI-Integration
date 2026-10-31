import os

import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

connection = snowflake.connector.connect(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("SNOWFLAKE_USER"),
    private_key_file="keys/ai_mcp_service.p8",
    private_key_file_pwd=os.getenv("SNOWFLAKE_PRIVATE_KEY_PASSPHRASE"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA"),
    role=os.getenv("SNOWFLAKE_ROLE"),
)

try:
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            TERRITORY,
            SUM(REVENUE) AS TOTAL_REVENUE
        FROM ENTERPRISE_AI.SALES.SALES_TRANSACTIONS
        GROUP BY TERRITORY
        ORDER BY TOTAL_REVENUE DESC
    """)

    for territory, revenue in cursor.fetchall():
        print(f"{territory}: ${revenue:,.2f}")

finally:
    cursor.close()
    connection.close()