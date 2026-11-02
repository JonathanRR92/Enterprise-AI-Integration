# Local setup and verification

This project was developed on Windows using PowerShell, Python 3.12, Snowflake, Salesforce Developer Edition and Claude Desktop.

## 1. Install Python dependencies

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Fill in `.env` with **your own** Snowflake and Salesforce values. `.env` is excluded by `.gitignore`.

## 2. Snowflake setup

Provision a database `ENTERPRISE_AI`, schema `SALES`, and table `SALES_TRANSACTIONS` with columns used by the queries: `TERRITORY`, `SALES_REP`, and `REVENUE`. The demonstration used **10 fictional transactions** totaling **$124,000**. The original seed SQL is not included in the uploaded source, so this repository does not claim to provide a reproducible data seed.

Create a dedicated service user (`AI_MCP_SERVICE`) and read-only role (`AI_SALES_READER`). Grant the role `USAGE` on warehouse `AI_DEV_WH`, database `ENTERPRISE_AI`, and schema `SALES`, plus `SELECT` on `SALES_TRANSACTIONS`. Configure RSA public-key authentication on the service user. Store the corresponding private key locally as `keys/ai_mcp_service.p8` and its passphrase in `.env`. Never upload the key or passphrase.

```powershell
python snowflake_test.py
```

Expected: a revenue summary grouped by territory. Errors can arise from missing warehouse `USAGE`, table `SELECT`, incorrect account identifiers, or invalid key-pair configuration.

## 3. Salesforce setup

In a Salesforce Developer Edition org:

1. Create an **External Client App** named `Enterprise AI Integration` with OAuth `api` scope and **Client Credentials Flow** enabled.
2. Create a dedicated Salesforce Integration user (example: `Enterprise AI Service`) with minimum API access.
3. Create a permission set (example: `Enterprise AI CRM Reader`) granting **read** permissions to `Account` and `Opportunity` objects and the intended fields; assign it to the integration user.
4. Set the External Client App **Run As** user to the integration user's **full Salesforce username**.
5. Add the app's Client ID and Client Secret and your Salesforce **My Domain** URL to `.env`.

```powershell
python salesforce.py
```

Expected: `Salesforce authentication successful!` This confirms **OAuth token acquisition only**, not access to Account records. The next development step is a Salesforce REST API query and permission test.

## Claude Desktop

In Claude Desktop's MCP configuration, add an entry equivalent to the following, adjusting both paths for your machine:

```json
{
  "mcpServers": {
    "enterprise-snowflake": {
      "command": "C:\path\to\Enterprise-AI-Integration\.venv\Scripts\python.exe",
      "args": ["C:\path\to\Enterprise-AI-Integration\server.py"]
    }
  }
}
```

Restart Claude Desktop and verify that `get_sales_by_territory` and `get_sales_by_representative` are discoverable. Ask Claude to run one of the tools. The server uses stdio; avoid adding `print()` statements to its normal execution path, as they can corrupt MCP messages.

## Local testing and troubleshooting

- `python -m py_compile server.py salesforce.py snowflake_test.py` checks syntax only.
- `python snowflake_test.py` requires live Snowflake credentials and warehouse permissions.
- `python salesforce.py` requires live Salesforce OAuth configuration.
- A successful Salesforce OAuth response **does not** guarantee object, field, or record access.
- Keep any logs or screenshots free of tokens, client secrets, private keys, and identifiable customer information.
