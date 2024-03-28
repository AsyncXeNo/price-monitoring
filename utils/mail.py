import os
from datetime import datetime, timedelta

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


def get_credentials():
    creds = None
    if os.path.exists('data/auth/token.json'):
        creds = Credentials.from_authorized_user_file('data/auth/token.json')
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'data/auth/client_secret.json',
                scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/gmail.send']
            )
            creds = flow.run_local_server(port=0)
        with open('data/auth/token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


print(get_credentials().expiry)
