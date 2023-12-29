# This program is going to download the top 10 songs from a music website, whenever the program is run.
# I don't want to download previously downloaded songs.
# I want to store the downloaded music in a folder
# I want to store the names of the songs in a file
# I want to reference the day file and then pull the file from the music folder to play.


# First, I need to find the API that is going to let me see and download the top 10 songs of the day.

# curl -X POST "https://accounts.spotify.com/api/token" \
#      -H "Content-Type: application/x-www-form-urlencoded" \
#      -d "grant_type=client_credentials&client_id=449201bb092d4a52adbcfcd97637dd94&client_secret=5dafd98e2e5c416498c9a2dfab8feacb"


#{"access_token":"BQCSr684oDgilveGYq51-wF9RmJIbEQ_2zIkDAmnofjM3YYy50dBduTHyHHs_ojWWZ_5zYb2vkK9JCPwgAuyNH_Trm6lZwIvBgcNtFhUwG79JiG3Fds","token_type":"Bearer","expires_in":3600}
import requests
import json

def authUser() -> str:
    authUrl = 'https://accounts.spotify.com/api/token'
    headers = {
        "Content-Type": 'application/x-www-form-urlencoded'
    }
    payload = {
        'grant-type': 'client_credentials',
        # These need to be hidden and moved
        'client_id':'449201bb092d4a52adbcfcd97637dd94',
        'client_secret': '5dafd98e2e5c416498c9a2dfab8feacb'
    }
    res = requests.post(url=authUrl, headers=headers, payload=payload)


# I'm going to check my auth code using this function
with open('auth.txt', 'r') as file:
    file_content = file.read()
    data = json.loads(file_content)

print(data)

url = "https://api.spotify.com/v1/me"
headers = {
    'Authorization': 'Bearer BQCSr684oDgilveGYq51-wF9RmJIbEQ_2zIkDAmnofjM3YYy50dBduTHyHHs_ojWWZ_5zYb2vkK9JCPwgAuyNH_Trm6lZwIvBgcNtFhUwG79JiG3Fds',
}
res = requests.get(url=url, headers=headers)
# If I get a successful response I want to see the response.
if res.status_code == 200:
    res_json = res.json()
    print(res_json)

else:
    if res.status_code == 401:
        new_auth = authUser()
        with open('auth.txt', 'w') as file:
            test_dict = {"Test": "Test"}
            # test_json = test_dict.json()

            json.dump(test_dict, file, indent=2)
    print(f"Error: {res.status_code}")
    print()
