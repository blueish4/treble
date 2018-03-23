from base64 import b64encode
from json import dump, load
from requests import post, get


# Return access_token
def get_access_token(client_id, client_secret):
    token_url = "https://accounts.spotify.com/api/token"

    # Must be encoded to get access token
    # encoded = b64encode(bytes(client_id + ':' + client_secret, "utf-8")).decode("ascii")
    encoded = b64encode(client_id + ':' + client_secret, "utf-8").encode("ascii")

    headers = {"Authorization": "Basic " + encoded}
    data = {"grant_type": "client_credentials"}

    response = post(token_url, data=data, headers=headers)

    return response.json()['access_token']


#  Get data for a given track_name from Spotify. Return the Response object
def get_data_from_spotify(search_term, search_type, access_token):
    search_url = "https://api.spotify.com/v1/search?q=" + search_type + \
                 ":" + search_term + "&type=" + search_type + "&limit=5"

    headers = {"Authorization": "Bearer " + access_token}
    response = get(search_url, headers=headers)

    return response


# Search the Spotify API for a given track_name. Return the JSON result
def search_spotify(search_term, search_type):
    # Open JSON file and read data into local dictionary
    with open('token.json', 'r') as json_file:
        token_dict = load(json_file)

    # Try to search Spotify API
    response = get_data_from_spotify(search_term, search_type, token_dict['ACCESS_TOKEN'])

    # If status_code is not 200, then:
    #       1. The access token has not been initialised OR
    #       2. The access token has expired (expires after 1 hour)
    if response.status_code != 200:
        # Get access token, then get data from Spotify
        token_dict['ACCESS_TOKEN'] = get_access_token(token_dict['CLIENT_ID'], token_dict['CLIENT_SECRET'])
        with open('token.json', 'w') as json_file:
            dump(token_dict, json_file)
        full_json = get_data_from_spotify(search_term, search_type, token_dict['ACCESS_TOKEN']).json()
        if search_type == "track":
            return process_json_track(full_json)
        else:
            return process_json_artist(full_json)
    else:
        # We have a valid access_token, so simply return the required data
        full_json = response.json()
        with open('token.json', 'w') as json_file:
            dump(token_dict, json_file)
        if search_type == "track":
            return process_json_track(full_json)
        else:
            return process_json_artist(full_json)


# Process JSON data to retrieve the information we need:
#       track_name, album, artist, artwork_url, spotify_uri
# Return this in JSON format
def process_json_track(json_in):
    json_to_return = []
    for song in json_in['tracks']['items']:
        song_info = {
            'track_name': song['name'],
            'album': song['album']['name'],
            'artist': song['artists'][0]['name'],
            'artwork_url': song['album']['images'][0]['url'],
            'spotify_uri': "spotify:track:" + song['id']
        }
        song_info['genre'] = get_genre(song_info['artist'])
        json_to_return.append(song_info)
    ret_value = {"tracks": json_to_return}
    return ret_value


# Process JSON data to retrieve the genre for a given song
def process_json_artist(json_in):
    return json_in['artists']['items'][0]['genres']


def get_genre(artist):
    return search_spotify(artist, "artist")
