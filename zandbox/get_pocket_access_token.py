import requests

# Replace 'YOUR_CONSUMER_KEY' and 'YOUR_REDIRECT_URI' with your actual consumer key and redirect URI
consumer_key = '111019-c0e83868129c3826322f20f'
redirect_uri = 'https://hci.prof'

# Step 1: Obtain a request token
url = 'https://getpocket.com/v3/oauth/request'
headers = {'Content-Type': 'application/json; charset=UTF-8', 'X-Accept': 'application/json'}
data = {'consumer_key': consumer_key, 'redirect_uri': redirect_uri}
response = requests.post(url, json=data, headers=headers)
request_token = response.json().get('code')

# Step 2: Redirect user to Pocket for authorization
auth_url = f"https://getpocket.com/auth/authorize?request_token={request_token}&redirect_uri={redirect_uri}"
print("Please go to this URL and authorize:", auth_url)

# Step 4: Convert the request token into an access token
url = 'https://getpocket.com/v3/oauth/authorize'
data = {'consumer_key': consumer_key, 'code': request_token}
response = requests.post(url, json=data, headers=headers)
access_token = response.json().get('access_token')
print("Your access token is:", access_token)
