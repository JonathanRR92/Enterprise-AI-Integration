import os
import requests

from pathlib import Path
from dotenv import load_dotenv


# Locate the project directory
PROJECT_DIR = Path(__file__).resolve().parent

# Load environment variables
load_dotenv(PROJECT_DIR / ".env")


def get_salesforce_token():

    # Retrieve Salesforce credentials
    instance_url = os.getenv("SALESFORCE_INSTANCE_URL")
    client_id = os.getenv("SALESFORCE_CLIENT_ID")
    client_secret = os.getenv("SALESFORCE_CLIENT_SECRET")

    # Verify required environment variables exist
    if not all([instance_url, client_id, client_secret]):
        raise ValueError("Missing Salesforce environment variables.")

    # Salesforce OAuth token endpoint
    token_url = f"{instance_url.rstrip('/')}/services/oauth2/token"

    # OAuth Client Credentials payload
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    # Send authentication request
    response = requests.post(
        token_url,
        data=payload,
        timeout=30
    )

    # Check for HTTP errors
    response.raise_for_status()

    # Convert JSON response into a Python dictionary
    token_data = response.json()

    # Extract and return the access token
    return token_data["access_token"]


def get_salesforce_accounts():

    # Step 1: Authenticate with Salesforce
    token = get_salesforce_token()

    # Step 2: Retrieve Salesforce instance URL
    instance_url = os.getenv("SALESFORCE_INSTANCE_URL").rstrip("/")

    # Step 3: Define our SOQL query
    query = """
        SELECT Id, Name, Industry, BillingCity, BillingState
        FROM Account
        WHERE Name = 'Pacific Tech Solutions'
        LIMIT 1
    """

    # Step 4: Salesforce REST API endpoint
    url = f"{instance_url}/services/data/v60.0/query"

    # Step 5: Include OAuth access token
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    # Step 6: Send GET request to Salesforce
    response = requests.get(
        url,
        headers=headers,
        params={"q": query},
        timeout=30
    )

    # Step 7: Check for HTTP errors
    response.raise_for_status()

    # Step 8: Extract Account records from JSON response
    return response.json()["records"]


# Test Salesforce authentication and Account retrieval
if __name__ == "__main__":

    try:
        # Test authentication
        token = get_salesforce_token()

        if token:
            print("Salesforce authentication successful!")

        # Test Account retrieval
        accounts = get_salesforce_accounts()

        if not accounts:
            print("No matching Salesforce accounts found.")

        for account in accounts:
            print("\nSalesforce Account Retrieved:")
            print("Account:", account["Name"])
            print("Industry:", account["Industry"])
            print("City:", account["BillingCity"])
            print("State:", account["BillingState"])

    except requests.exceptions.HTTPError as error:
        print(
            "Salesforce API HTTP error:",
            error.response.status_code
        )

    except requests.exceptions.RequestException as error:
        print(
            f"Salesforce request failed: {type(error).__name__}"
        )

    except (ValueError, KeyError, TypeError) as error:
        print(
            f"Salesforce configuration or response error: {type(error).__name__}"
        )