import requests
from google.oauth2.credentials import Credentials

# Twitter API keys
twitter_consumer_key = "Your Twitter API key"# Replace these values with your API keys
twitter_consumer_secret = "Your Twitter API secret key"# Replace these values with your API secret keys
twitter_access_token = "Your Twitter access token"# Replace these values with your access token
twitter_access_token_secret = "Your Twitter access token secret"# Replace these values with your access token secret

# LinkedIn API keys
linkedin_client_id = "Your LinkedIn API key"# Replace these values with your API keys
linkedin_client_secret = "Your LinkedIn API secret key"# Replace these values with your API secret keys

# Replace these values with your client ID and client secret
google_client_id = "Your Google API key"# Replace these values with your API keys   
google_client_secret = "Your Google API secret key"# Replace these values with your API secret keys

# Set the OAuth 2.0 authorization endpoint and parameters
google_auth_endpoint = "https://accounts.google.com/o/oauth2/v2/auth"
google_auth_params = {
    "client_id": google_client_id,
    "response_type": "code",
    "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
    "scope": "https://www.googleapis.com/auth/spreadsheets",
}

# Set the authentication headers for the LinkedIn API
linkedin_headers = {
    "X-Restli-Protocol-Version": "2.0.0",
}

# Set the blacklist of accounts to ignore
blacklist = ["bad_account_1", "bad_account_2"]

# Set the keyword to filter by
keyword = "keyword"

# Set the list of LinkedIn and Twitter accounts to monitor
linkedin_accounts = ["urn:li:person:abcdefghijkl"]
twitter_accounts = ["youUserName"]

# Load the OAuth 2.0 credentials
creds = Credentials.from_authorized_user_info(info=google_auth_params)

# Set the Google Sheets API endpoint and parameters
sheets_endpoint = "https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{range}:append"
sheets_params = {
    "valueInputOption": "RAW",
}

# Set the Twitter API endpoint
twitter_endpoint = "https://api.twitter.com/1.1/statuses/user_timeline.json"

# Set the LinkedIn API endpoint
linkedin_endpoint = "https://api.linkedin.com/v2/ugcPosts"

while True:
    # Iterate over the LinkedIn accounts
    for account in linkedin_accounts:
              # Set the LinkedIn API request parameters
        linkedin_params = {
            "q": "authors",
            "authors": [account],
            "count": 10,
        }

        # Make a GET request to the LinkedIn API endpoint
        linkedin_response = requests.get(linkedin_endpoint, params=linkedin_params, headers=linkedin_headers)

        # Check the status code of the response
        if linkedin_response.status_code == 200:
            # Parse the JSON data in the response
            linkedin_data = linkedin_response.json()

            # Iterate over the LinkedIn posts
            for post in linkedin_data["elements"]:
                # Check if the user's bio or title contains the keyword
                if keyword in post["author"]["bio"]["text"] or keyword in post["author"]["title"]:
                    # Set the values for the new row
                    values = [
                        post["creationTimestamp"],
                        post["author"]["firstName"] + " " + post["author"]["lastName"],
                        post["summary"]["text"],
                    ]

                    # Set the data for the request body
                    data = {
                        "values": [values]
                    }

                    # Make a POST request to the Google Sheets API endpoint
                    sheets_response = requests.post(sheets_endpoint, params=sheets_params, json=data, headers={"Authorization": f"Bearer {creds.token}"})

                    # Check the status code of the response
                    if sheets_response.status_code == 200:
                        print("LinkedIn post added to Google Sheets")
                    else:
                        print("Error adding LinkedIn post to Google Sheets")

    # Iterate over the Twitter accounts
    for account in twitter_accounts:
        # Set the Twitter API request parameters
        twitter_params = {
            "screen_name": account,
            "count": 10,
        }

        # Make a GET request to the Twitter API endpoint
        twitter_response = requests.get(twitter_endpoint, params=twitter_params, auth=(twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_token_secret))

        # Check the status code of the response
        if twitter_response.status_code == 200:
            # Parse the JSON data in the response
            twitter_data = twitter_response.json()

            # Iterate over the tweets
            for tweet in twitter_data:
                # Check if the account is blacklisted
                if tweet["user"]["screen_name"] not in blacklist:
                    # Check if the user's bio or title contains the keyword
                    if keyword in tweet["user"]["description"] or keyword in tweet["user"]["name"]:
                        # Set the values for the new row
                        values = [
                            tweet["created_at"],
                            tweet["user"]["screen_name"],
                            tweet["text"],
                        ]

                        # Set the data for the request body
                        data = {"values": [values]
                        }

                        # Make a POST request to the Google Sheets API endpoint
                        sheets_response = requests.post(sheets_endpoint, params=sheets_params, json=data, headers={"Authorization": f"Bearer {creds.token}"})

                        # Check the status code of the response
                        if sheets_response.status_code == 200:
                            print("Twitter tweet added to Google Sheets")
                        else:
                            print("Error adding Twitter tweet to Google Sheets")


                
