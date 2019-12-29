import os
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


class Credentials:
    """A class to create and hold credentials needed to interact with the gmail interface
    """

    def __init__(self):
        self.__scopes = ['https://www.googleapis.com/auth/gmail.modify']
        self.__creds = self.__create_credentials(self.__scopes)

        self.__service = build('gmail', 'v1', credentials=self.__creds)

    def __create_credentials(self, scopes):
        """Creates the necessary credentials to interact with gmail api. These
        are saved to token.pickle or if token.pickle already exist, then they are
        read from token.pickle

        Returns:
            Credentials for Gmail Api in a google Resource object.
        """
        creds = None

        # The File token.pickle stores the user's access and refresh tokens,
        # and is created automatically whne the flow compleates for the first time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # if there are no valid credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', scopes)
                creds = flow.run_local_server(port=0)
            # save the creds for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return creds

    def get_service(self):
        """A method to get the service instance needed to communicate with the gmail api

        Returns: An instance of the GmailApiClient service
        """
        return self.__service
