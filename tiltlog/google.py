from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

class Store:

    def __init__(self, spreadsheet_id=None):
        self.spreadsheet_id = spreadsheet_id
        self.credentials = Credentials.from_service_account_file(
            'credentials.json',
            scopes=SCOPES,
        )

        self.service = build('sheets', 'v4', credentials=self.credentials)


    def append(self, data):
        result = self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range="Sheet1!A:E",
            valueInputOption="USER_ENTERED",
            body={
                'values': data,
            }
        ).execute()
