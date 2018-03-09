import requests
import base64
import json


# Return access_token
def get_access_token(client_id, client_secret):
    token_url = "https://accounts.spotify.com/api/token"

    # Must be encoded to get access token
    encoded = base64.b64encode(client_id + ':' + client_secret).encode('ascii')

    headers = {"Authorization": "Basic " + encoded}
    data = {"grant_type": "client_credentials"}

    response = requests.post(token_url, data=data, headers=headers)

    return response.json()['access_token']


#  Get data for a given track_name from Spotify. Return the Response object
def get_data_from_spotify(track_name, access_token):
    search_url = "https://api.spotify.com/v1/search?q=track:" + track_name + "&type=track&limit=5"

    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get(search_url, headers=headers)

    return response


# Search the Spotify API for a given track_name. Return the JSON result
def search_spotify(track_name):
    # Open JSON file and read data into local dictionary
    json_file = open('token.json', 'r')
    token_dict = json.load(json_file)


    # Try to search Spotify API
    response = get_data_from_spotify(track_name, token_dict['ACCESS_TOKEN'])

    # If status_code is not 200, then:
    #       1. The access token has not been initialised OR
    #       2. The access token has expired (expires after 1 hour)
    if response.status_code != 200:
        # Get access token, then get data from Spotify
        token_dict['ACCESS_TOKEN'] = get_access_token(token_dict['CLIENT_ID'], token_dict['CLIENT_SECRET'])
        json_file = open('token.json', 'w')
        json.dump(token_dict, json_file)
        full_json = get_data_from_spotify(track_name, token_dict['ACCESS_TOKEN']).json()
        return process_json(full_json)
    else:
        # We have a valid access_token, so simply return the required data
        full_json = response.json()
        json_file = open('token.json', 'w')
        json.dump(token_dict, json_file)
        return process_json(full_json)


# Process JSON data to retrieve the information we need:
#       track_name, album, artist, artwork_url, spotify_uri
# Return this in JSON format
def process_json(json):
    json_to_return = []
    for song in json['tracks']['items']:
        song_info = {
            'track_name': song['name'],
            'album': song['album']['name'],
            'artist': song['artists'][0]['name'],
            'artwork_url': song['album']['images'][0]['url'],
            'spotify_uri': "spotify:track:" + song['id']
        }
        json_to_return.append(song_info)

    # Display final array **FOR TESTING**
    print(json_to_return)

    return json_to_return



# Test
search_spotify('Counting Stars')
