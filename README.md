<<<<<<< HEAD
# JML Identity Lifecycle Automation

A Python-based joiner/mover/leaver (JML) automation tool that connects to Microsoft Graph API to manage user identity lifecycle events in real time. Built as a hands-on identity engineering lab to demonstrate enterprise IAM automation patterns.

---

## The Problem This Solves

Manual provisioning is slow, inconsistent, and a security liability. In most environments:

- New hires wait days for access that should be ready on day one
- Movers keep permissions from their old role indefinitely
- Leavers stay active in the directory long after their last day

This tool automates all three events from a structured HR input, executes changes via Microsoft Graph API, revokes sessions on deactivation, and produces a full audit log of every action taken.

---

## Architecture

```
hr_events.csv
      |
      v
jml_automation.py       <-- orchestration layer
      |
      v
graph_users.py          <-- user operations (create, update, deactivate)
      |
      v
graph_auth.py           <-- MSAL token acquisition
      |
      v
Microsoft Graph API     <-- Entra ID / Microsoft 365
      |
      v
jml_audit.log           <-- immutable audit trail
```

**Auth flow:** MSAL client credentials grant (app-only, no user context required)

**Identity provider:** Microsoft Entra ID (Azure AD)

---

## Features

- Create users with temporary password and force-change on first login
- Update department and manager on role change
- Deactivate accounts and immediately revoke all active sessions
- Full audit log with timestamps for every action
- Run summary showing create / update / deactivate / failure counts
- Error handling that logs failures without stopping the rest of the run

---

## Project Structure

```
jml-identity-automation/
├── jml_automation.py       # Main orchestration script
├── graph_users.py          # Microsoft Graph user operations
├── graph_auth.py           # MSAL authentication module
├── hr_events.csv           # Sample HR input file
├── jml_audit.log           # Generated audit log (gitignored)
├── .env                    # Credentials (gitignored)
├── .env.example            # Credential template
├── .gitignore
└── README.md
```

---

## Prerequisites

- Python 3.8+
- Microsoft 365 developer tenant (free at developer.microsoft.com/microsoft-365/dev-program)
- App registration in Microsoft Entra ID with the following permissions:
  - `User.ReadWrite.All` (Application)
  - `Group.Read.All` (Application)
  - `AuditLog.Read.All` (Application)
- Admin consent granted on all permissions

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/yourusername/jml-identity-automation
cd jml-identity-automation
```

**2. Install dependencies**
```bash
pip install msal requests python-dotenv
```

**3. Configure credentials**
```bash
cp .env.example .env
```

Edit `.env` with your values:
```
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret
AZURE_TENANT_ID=your-tenant-id
```

**4. Prepare your HR events file**

Edit `hr_events.csv` using this format:
```
action,first_name,last_name,email,department,manager,start_date,end_date
create,Jane,Smith,jsmith@yourdomain.onmicrosoft.com,Engineering,manager@yourdomain.com,2024-01-15,
update,Jane,Smith,jsmith@yourdomain.onmicrosoft.com,Security,newmanager@yourdomain.com,,
deactivate,Jane,Smith,jsmith@yourdomain.onmicrosoft.com,,,,2024-06-01
```

**5. Run the script**
```bash
python jml_automation.py
```

---

## Sample Output

```
Created: jsmith@yourdomain.onmicrosoft.com
Updated: jsmith@yourdomain.onmicrosoft.com
Sessions revoked: jsmith@yourdomain.onmicrosoft.com
Deactivated: jsmith@yourdomain.onmicrosoft.com

--- JML Run Summary ---
Created:     1
Updated:     1
Deactivated: 1
Failed:      0
----------------------
```

---

## Sample Audit Log

```
2024-01-15 08:32:11 - INFO - CREATE SUCCESS: jsmith@yourdomain.onmicrosoft.com
2024-03-01 09:14:22 - INFO - UPDATE SUCCESS: jsmith@yourdomain.onmicrosoft.com moved to Security
2024-06-01 17:00:03 - INFO - DEACTIVATE SUCCESS: jsmith@yourdomain.onmicrosoft.com
2024-06-01 17:00:04 - INFO - SESSIONS REVOKED: jsmith@yourdomain.onmicrosoft.com
```

---

## Security Decisions

**Why application permissions instead of delegated?**
This script runs as a scheduled process with no user context. Delegated permissions require an interactive user session, which breaks automation. Application permissions with a service principal is the correct pattern for unattended lifecycle management.

**Why revoke sessions on deactivation?**
Disabling an account prevents new logins but does not terminate active sessions. A leaver with an open browser session retains access until the token expires, typically one hour. Revoking sessions on deactivation closes that window immediately.

**Why force password change on create?**
The script sets a temporary password to provision the account. Forcing a change on first login ensures the admin never knows the user's actual password and the user controls their own credentials from day one.

**Why log every action?**
Every create, update, deactivate, and failure is written to an audit log with a timestamp. This mirrors the evidence collection pattern required for SOC 2 and HIPAA access control audits.

---

## What I'd Add in Production

- Pull HR events from a real HRIS (Workday, BambooHR) via API instead of CSV
- Add an approval workflow before executing create events
- Notify the user's manager on deactivation with a confirmation receipt
- Schedule execution with a cron job or Azure Function triggered by HR system webhooks
- Add group membership management so movers are added to new role groups and removed from old ones automatically
- Store audit logs in a SIEM instead of a local file
- Use Azure Key Vault instead of a .env file for credential storage
- Add idempotency checks so re-running the script on the same CSV doesn't duplicate actions

---

## Frameworks and Concepts Demonstrated

- Identity lifecycle management (joiner, mover, leaver)
- Microsoft Graph API integration
- MSAL client credentials authentication flow
- Least privilege access (application permissions scoped to minimum required)
- Session revocation on offboarding
- Audit logging for compliance evidence
- Python automation for identity operations

---

## Author

Priscilla Lopez
CISSP | GCPN | GCHFI
linkedin.com/in/p-g-lopez
=======
# jml-identity-automation
>>>>>>> bd8a22a669f70bd0fb5964f9712481ed2377e78c
