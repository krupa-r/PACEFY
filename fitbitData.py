import requests

LIENT_ID = '23PSWZ'
CLIENT_SECRET = '7f8e7499733da03773fa9a67780c92cc'
REDIRECT_URI = 'http://localhost:4040/callback'

access_token = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyM1BUSlMiLCJzdWIiOiJCMlJIR0ciLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJlY2cgcnNldCByaXJuIHJveHkgcnBybyBybnV0IHJzbGUgcmNmIHJhY3QgcnJlcyBybG9jIHJ3ZWkgcmhyIHJ0ZW0iLCJleHAiOjE3MjgyMTA2NTgsImlhdCI6MTcyODE4MTg1OH0.ZRA5ooumuRdsffu_QOAKk3jSynU-ymTLB3U9FJQIN6A'
refresh_token = '061023f408240e726e629d8a764b651bf11b913d6442c20f9f149452ceab1a48'


headers = {'Authorization': 'Bearer' + access_token}
# Fitbit API endpoint to fetch heart rate data (1-minute interval for today)
url = 'https://api.fitbit.com/1/user/-/activities/heart/date/today/1d/1min.json'

# Make the API request to fetch heart rate data
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    print("Heart Rate Data:")
    print(response.json())  # Display the heart rate data
else:
    print(f"Error: {response.status_code}")
    print(response.json())  # Print the error message from the API