# Project roadmap

## Completed and tested

- [x] Created Snowflake warehouse, database, schema and fictional sales transaction data.
- [x] Configured Snowflake service user, reader role, RSA key-pair authentication and warehouse access.
- [x] Built Python MCP server with revenue-by-territory and revenue-by-representative tools.
- [x] Connected MCP server to Claude Desktop and tested Snowflake analytics.
- [x] Created Salesforce External Client App and dedicated API integration user.
- [x] Assigned read-only Account and Opportunity permissions via a permission set.
- [x] Successfully acquired a Salesforce OAuth 2.0 client-credentials token from Python.

## Next milestone: Salesforce data retrieval

- [ ] Add a restricted Salesforce REST/SOQL query to retrieve the fictional **Pacific Tech Solutions** Account.
- [ ] Verify `Account` object, field-level and record-level permissions, including `BillingCity` and `BillingState` API behavior.
- [ ] Handle missing records, HTTP errors and safe token use.

## Upcoming MCP integration

- [ ] Expose `get_salesforce_accounts()` as a read-only MCP tool.
- [ ] Verify the Salesforce tool in MCP Inspector and Claude Desktop.
- [ ] Add Opportunity retrieval with least-privilege access.
- [ ] Combine Snowflake historical revenue with Salesforce CRM pipeline data.
- [ ] Add unit tests, seeded demonstration data and reproducible setup automation.
- [ ] Add sanitized screenshots of real MCP tool executions.

**Status discipline:** Authentication is not the same as data authorization. Salesforce REST queries and cross-platform AI analysis remain planned until actually tested.
