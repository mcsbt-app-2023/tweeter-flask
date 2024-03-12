# %%
import requests
from requests.auth import HTTPBasicAuth


def create_user_password(username, password):
    return {
        "username": username,
        "password": password,
    }


def create_url(path):
    return "http://localhost:8080" + path


requests.post(
    create_url("/users"),
    json={
        "username": "pepepe",
        "password": "pepepe",
    },
)


# authentication = HTTPBasicAuth("other", "other")

# response = requests.get(create_url("/users"), auth=authentication)

# if response.status_code == 200:
#     for user in response.json():
#         print(user)
# else:
#     print("authenticate first, please")
# # %%
