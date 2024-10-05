from flask import Flask, render_template, request, redirect, url_for
from spotipy import *
from spotipy.oauth2 import SpotifyOAuth

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
