import requests
import json

def get_access_token():
    url = "https://id.kiotviet.vn/connect/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "scopes": "PublicApi.Access",
        "grant_type": "client_credentials",
        "client_id": "3b95665a-8c28-492f-85f5-d1a095e541a9",
        "client_secret": "7AC17E477F3BAAD3F9E3F42EB292B9BFBA4F9F95"
    }
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json().get("access_token")

def get_users(access_token, retailer, current_item, page_size):
    url = "https://public.kiotapi.com/users"
    headers = {
        "Retailer": retailer,
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "currentItem": current_item,
        "pageSize": page_size
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def get_branches(access_token, retailer, current_item, page_size):
    url = "https://public.kiotapi.com/branches"
    headers = {
        "Retailer": retailer,
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "currentItem": current_item,
        "pageSize": page_size,
        "includeRemoveIds": "false"
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def write_to_firebase(url, data):
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.put(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    return response.json()

def fetch_and_store_users(access_token, retailer):
    current_item = 0
    page_size = 100
    all_users = []

    while True:
        data = get_users(access_token, retailer, current_item, page_size)
        users = data.get("data", [])

        for user in users:
            user_data = {"id": user.get("id"), "givenName": user.get("givenName")}
            all_users.append(user_data)

        if len(users) < page_size:
            break

        current_item += page_size

    write_to_firebase("https://emall-1ad4b-default-rtdb.firebaseio.com/TB01.json", all_users)

def fetch_and_store_branches(access_token, retailer):
    current_item = 0
    page_size = 100
    all_branches = []

    while True:
        data = get_branches(access_token, retailer, current_item, page_size)
        branches = data.get("data", [])

        for branch in branches:
            branch_data = {"id": branch.get("id"), "branchName": branch.get("branchName")}
            all_branches.append(branch_data)

        if len(branches) < page_size:
            break

        current_item += page_size

    write_to_firebase("https://emalluserbranch-default-rtdb.asia-southeast1.firebasedatabase.app/02.json", all_branches)

def main():
    access_token = get_access_token()
    retailer = "ifd"

    fetch_and_store_users(access_token, retailer)
    fetch_and_store_branches(access_token, retailer)

if __name__ == "__main__":
    main()
