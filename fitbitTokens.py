import requests
from requests_oauthlib import OAuth2Session

CLIENT_ID = '23PTJR'
CLIENT_SECRET = '991e805111c62053457a518654f0c8fe'
REDIRECT_URI = 'https://localhost:5000/callback'

# Authorization URL and token URL
AUTH_URL = 'https://www.fitbit.com/oauth2/authorize'
TOKEN_URL = 'https://api.fitbit.com/oauth2/token'

# Step 1: Get authorization URL
fitbit = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=['activity','heartrate','respiratory_rate'])
authorization_url, state = fitbit.authorization_url(AUTH_URL)

# print('Please go to {} and authorize access.'.format(authorization_url))

print('Please go to this url and authorize access:')
print(authorization_url)

# Step 2: Once authorized, Fitbit will redirect you to the REDIRECT_URI with a code in the URL
# Use the code to fetch the access token
response_url = input('Paste the full redirect URL here: ')

# Step 3: Fetch the access token
token = fitbit.fetch_token(TOKEN_URL, authorization_response=response_url,client_id = CLIENT_ID, client_secret=CLIENT_SECRET)

#Print access token and refresh token
print('Access token:', token['access_token'])
print('Refresh token:', token['refresh_token'])

ACCESS_TOKEN = token['access_token']
REFRESH_TOKEN = token['refresh_token']
