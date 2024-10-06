from flask import Flask, render_template, request, redirect, url_for
from spotipy import *
from spotipy.oauth2 import SpotifyOAuth
import time

app = Flask(__name__)

# Spotify Developer credentials
SPOTIPY_CLIENT_ID = '19fa65ae572f4e1b8b23b2620a7c26fc'
SPOTIPY_CLIENT_SECRET = 'aac5b5c464234278b5058f0e11476f2f'
SPOTIPY_REDIRECT_URI = 'http://localhost:5000/callback'

# Set up Spotify authentication scope
sp_oauth = SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope="user-modify-playback-state,user-read-playback-state"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play', methods=['POST'])
def play_song():
    track_uri = request.form['track_uri']
    
    # Get Spotify token
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        return redirect(url_for('authorize'))
    
    sp = Spotify(auth=token_info['access_token'])
    
    # Play the track
    try:
        sp.start_playback(uris=[track_uri])
        return "Playing song!"
    except Exception as e:
        return str(e)


is_running = False

@app.route("/songsRetrieve", methods=['POST'])
def retrieve():
    global is_running
    bpm = 100
    # Get Spotify token
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        return redirect(url_for('authorize'))
    
    sp = Spotify(auth=token_info['access_token'])

    data = request.get_json()
    is_running = data.get('isRunning', False)  # Get the value from the frontend

    
    def get_artist_ids(artist_names):
        artist_ids = []
        for name in artist_names:
            results = sp.search(q=name, type='artist', limit=1)
            if results['artists']['items']:
                artist_ids.append(results['artists']['items'][0]['id'])
        return artist_ids

    # Get artist IDs for Karan Aujla and Diljit Dosanjh
    artist_names = ['Karan Aujla'] #'Diljit Dosanjh', 'Arijit Singh', 'Badshah'
    seed_artist_ids = get_artist_ids(artist_names)

    # Suggest songs
    recommendations = sp.recommendations(
        limit=100,
        seed_artists = seed_artist_ids,
        min_tempo=bpm,# Example seed genre
    )

    track_uri = recommendations['tracks'][0]["uri"]

    #Extract urls for the image for the songs
    image_urls = []
    for track in recommendations['tracks']:
        if 'album' in track and 'images' in track['album']:
            if track['album']['images']:
                image_urls.append(track['album']['images'][0]['url'])

    # return{"image_urls":image_urls}

    #Extract urls for the songs
    song_urls = []
    for track in recommendations['tracks']:
        if 'external_urls' in track:
                song_urls.append(track['external_urls']['spotify'])

    # return{"song_urls":song_urls}

    # try:
    #     sp.start_playback(uris=[track_uri])
    #     return "Playing song!"
    # except Exception as e:
    #     return str(e)

    #return recommendations["tracks"]
    
    i = 0
    while is_running and i<100: 
        track_uri = recommendations['tracks'][i]["uri"]
        try:
            sp.start_playback(uris=[track_uri])
            i+=1
            time.sleep(15)
            data = request.get_json()
            is_running = data.get('isRunning', False) 
        except Exception as e:
            return str(e)
    return "Thank You"

@app.route('/authorize')
def authorize():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
