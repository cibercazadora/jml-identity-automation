import requests
from graph_auth import get_headers, GRAPH_URL
import logging

logging.basicConfig(
    filename='jml_audit.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def create_user(user):
    payload = {
        "accountEnabled": True,
        "displayName": f"{user['first_name']} {user['last_name']}",
        "mailNickname": user['email'].split('@')[0],
        "userPrincipalName": user['email'],
        "department": user['department'],
        "passwordProfile": {
            "forceChangePasswordNextSignIn": True,
            "password": "TempPass123!"
        }
    }
    response = requests.post(
        f"{GRAPH_URL}/users",
        headers=get_headers(),
        json=payload
    )
    if response.status_code == 201:
        logging.info(f"CREATE SUCCESS: {user['email']}")
        print(f"Created: {user['email']}")
    else:
        logging.error(f"CREATE FAILED: {user['email']} - {response.json()}")
        print(f"Failed to create: {user['email']} - {response.json()}")

def update_user(user):
    response = requests.get(
        f"{GRAPH_URL}/users/{user['email']}",
        headers=get_headers()
    )
    if response.status_code != 200:
        logging.error(f"UPDATE FAILED - User not found: {user['email']}")
        return

    payload = {
        "department": user['department'],
    }
    if user['manager']:
        payload["manager@odata.bind"] = f"{GRAPH_URL}/users/{user['manager']}"

    response = requests.patch(
        f"{GRAPH_URL}/users/{user['email']}",
        headers=get_headers(),
        json=payload
    )
    if response.status_code == 204:
        logging.info(f"UPDATE SUCCESS: {user['email']} moved to {user['department']}")
        print(f"Updated: {user['email']}")
    else:
        logging.error(f"UPDATE FAILED: {user['email']} - {response.json()}")
        print(f"Failed to update: {user['email']}")

def deactivate_user(user):
    payload = {
        "accountEnabled": False
    }
    response = requests.patch(
        f"{GRAPH_URL}/users/{user['email']}",
        headers=get_headers(),
        json=payload
    )
    if response.status_code == 204:
        logging.info(f"DEACTIVATE SUCCESS: {user['email']}")
        print(f"Deactivated: {user['email']}")
        revoke_sessions(user['email'])
    else:
        logging.error(f"DEACTIVATE FAILED: {user['email']} - {response.json()}")
        print(f"Failed to deactivate: {user['email']}")

def revoke_sessions(email):
    response = requests.post(
        f"{GRAPH_URL}/users/{email}/revokeSignInSessions",
        headers=get_headers()
    )
    if response.status_code == 200:
        logging.info(f"SESSIONS REVOKED: {email}")
        print(f"Sessions revoked: {email}")
    else:
        logging.error(f"SESSION REVOKE FAILED: {email}")