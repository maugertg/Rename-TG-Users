import requests


def whoami(session, tg_host):
    """Query Threat Grid whoami for the provided API Key"""
    url = f"https://{tg_host}/api/v3/session/whoami"
    return session.get(url)


def get_users(session, tg_host, org_id):
    """Get list of users in Threat Grid org"""
    url = f"https://{tg_host}/api/v3/organizations/{org_id}/users"
    return session.get(url)


def rename_user(session, tg_host, login, new_name):
    """Rename the provided user"""
    url = f"https://{tg_host}/api/v3/users/{login}"
    body = {"name": new_name}
    return session.put(url, data=body)


def main():
    """Main script logic"""

    # Enter Threat Grid API Key
    tg_api_key = "asdf123asdf123asdf123"

    # Mapping of Login to New Name
    name_mapping = {
        "login1": "wsa1.example.org",
        "login2": "wsa2.example.org",
        "login3": "wsa3.example.org",
    }

    # Instantiate Threat Grid Session Object and set API Key
    tg_session = requests.Session()
    tg_session.params.update({"api_key": tg_api_key})
    tg_host = "panacea.threatgrid.com"

    # Get Org ID
    org_id = whoami(tg_session, tg_host).json().get("data", {}).get("organization_id")

    # Get Users from Org
    users = get_users(tg_session, tg_host, org_id).json().get("data", {}).get("users")

    # Check if a login is in the name mapping, if it is rename it to the new name
    for user in users:
        login = user.get("login", "")
        if login in name_mapping:
            print(f"Renaming {login} - ", end="")

            # Update the name the users
            response = rename_user(tg_session, tg_host, login, name_mapping[login])

            # Check the status
            if response.status_code == 204:
                print("Success!")
            else:
                print("Something went wrong!")


if __name__ == "__main__":
    main()
