# Security and least privilege

## Current controls

- **Snowflake:** dedicated service identity (`AI_MCP_SERVICE`), reader role (`AI_SALES_READER`), RSA private-key authentication, fixed SELECT-only queries.
- **Salesforce:** dedicated API integration user, OAuth 2.0 client credentials, read-only object permission set for Accounts and Opportunities.
- **Local secrets:** environment variables in `.env` and Snowflake key files in `keys/`; both excluded by `.gitignore`.
- **MCP:** tool functions expose specific analytics rather than accepting arbitrary SQL.

## What must never be committed

- `.env` or other files containing real client IDs, client secrets, passwords or access tokens.
- Snowflake private keys (`.p8`, `.pem`, `.key`) or key directories.
- Screenshots showing credentials, tokens or real customer information.
- A full `.git` directory copied from another machine or repository when distributing source ZIP files.

> **Security note for this project:** The source ZIP provided for the documentation refresh contained a real `.env` file and private-key material. The distributed portfolio ZIP **intentionally excludes both**. Review your local Git history and remote repository for accidental exposure. If a credential or private key has been publicly exposed, rotate/revoke it and remove it from history as appropriate; adding `.gitignore` afterward does not erase earlier commits.

## Verification before publishing

```powershell
git status --short
git ls-files .env keys
git diff --cached --name-only
```

The second command should return **no tracked secrets**. Review the staged file list before every commit. Avoid sharing terminal output that includes secret values.

## Future hardening

- Replace long-lived local secrets with a managed secret store for deployments.
- Add token expiration handling and safe error messages.
- Restrict Salesforce queries to necessary objects and fields; verify record sharing.
- Add automated secret scanning and tests before production use.
