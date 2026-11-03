# Enterprise AI Integration

A Python-based enterprise AI integration project that connects
Claude Desktop to Salesforce CRM and Snowflake through the
Model Context Protocol (MCP).

## Overview

This project demonstrates how AI assistants can securely access
business information from multiple enterprise platforms.

It uses a custom Python MCP server to expose read-only tools
for retrieving CRM records and analyzing sales performance.

## Technologies

- Python
- Model Context Protocol (MCP)
- Claude Desktop
- Salesforce REST API
- Salesforce OAuth 2.0
- Snowflake
- Snowflake Python Connector
- SOQL and SQL

## Architecture

Claude Desktop
    |
    v
Python MCP Server
    |
    +-- Salesforce REST API
    |      |
    |      +-- OAuth 2.0 Authentication
    |      +-- CRM Account Data
    |
    +-- Snowflake Connector
           |
           +-- Key-Pair Authentication
           +-- Sales Analytics

## Implemented MCP Tools

### get_crm_accounts
Retrieves Salesforce account information, including company
name, industry, and billing location.

Current implementation retrieves a configured sample account.

### get_sales_by_territory
Retrieves sales performance grouped by territory from Snowflake.

### get_sales_by_representative
Retrieves sales performance grouped by sales representative
from Snowflake.

## Security

- Salesforce OAuth 2.0 client credentials authentication
- Dedicated Salesforce integration identity
- Read-only Salesforce permissions
- Snowflake key-pair authentication
- Restricted Snowflake database role
- Credentials stored outside source control
- Read-only MCP tools

## Example AI Queries

"Retrieve our Salesforce CRM account information."

"Show total sales revenue by territory."

"Which sales representative generated the most revenue?"

"Compare Salesforce account locations with Snowflake
sales performance by territory."

## Project Status

Version 1.0 — Functional prototype

Successfully implemented Salesforce and Snowflake integrations
through a custom Python MCP server.

Future improvements include:
- Dynamic Salesforce account queries
- Salesforce Opportunity integration
- Expanded cross-platform analytics
- Error handling and logging
- Automated integration testing