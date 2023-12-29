import requests
import json
import datetime

# Saves New Auth Token to File
def save_auth(auth_token):
    with open('auth.txt', 'w') as file:
            json.dump(auth_token, file, indent=2)

# Run the Auth API to get new token
def authUser():
    authUrl = 'https://accounts.spotify.com/api/token'
    headers = {
        "Content-Type": 'application/x-www-form-urlencoded'
    }

    with open('secrets.json') as json_file:
         data = json.load(json_file)

    payload = {
        'grant_type': 'client_credentials',

        # These need to be hidden and moved
        'client_id': data['Credentials']['client_id'],
        'client_secret': data['Credentials']['client_secret']
    }
    res = requests.post(url=authUrl, headers=headers, data=payload)
    new_auth_json = res.json()
    print(new_auth_json)
    save_auth(new_auth_json)
    # I should get a access token json from this

# Returns Date string for file creation
def getDate():
    today = datetime.date.today()
    return today

# I'm going to check my auth code using this function
try:
    with open('auth.txt', 'r') as file:
        file_content = file.read()
        data = json.loads(file_content)
    access_token = data['access_token']
    token_type = data['token_type']
    url = 'https://api.spotify.com/v1/recommendations?seed_genres=hip-hop%2Ccountry'
    headers = {
        'Authorization': f"{token_type} {access_token}",
    }
    res = requests.get(url=url, headers=headers)
    # If I get a successful response I want to see the response.
    if res.status_code == 200:
        res_json = res.json()
        tracks = res_json['tracks']
        recommended_tracks = dict()
        for i, track in enumerate(tracks):
            artist = track['artists'][0]['name']
            title =  track['name']
            recommended_tracks[i+1] = artist + ": " + title

        todays_date = getDate()
        with open(f'./recommendations/{todays_date}.txt', 'w') as file:
            json.dump(recommended_tracks, file, indent=2)

    else:
        if res.status_code == 401:
            print("I need to get a new auth code")
            authUser()
except Exception as e:
    print("Need some auth credentials")
    authUser()