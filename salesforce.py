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


# Test Salesforce authentication
if __name__ == "__main__":

    try:
        token = get_salesforce_token()

        if token:
            print("Salesforce authentication successful!")

    except requests.exceptions.RequestException as error:
        print(f"Salesforce authentication failed: {type(error).__name__}")

    except (ValueError, KeyError) as error:
        print(f"Salesforce configuration or response error: {type(error).__name__}")