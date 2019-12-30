import pickle
import os.path
import time

import email
from email.mime.text import MIMEText
import base64

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import errors


class Event:
    """A basic Event class
    """

    def __init__(self):
        self.__handlers = []

    def __iadd__(self, handler):
        self.__handlers.append(handler)
        return self

    def __isub__(self, handler):
        self.__handlers.remove(handler)
        return self

    def __call__(self, *args, **kwargs):
        for handler in self.__handlers:
            print(handler.__name__)
            handler(*args, **kwargs)


class Watcher:
    """Monitors for changes in the inbox.

    Args: 
        service: A googleApiClient service instance
        handlers: Callback functions to handle events
    """

    def __init__(self, service, handler):
        self.__source = "Watcher: "

        self.__user_id = 'Wifi.Robot.Overlord@gmail.com'

        self.__service = service

        self.__emails = self.__get_emails()
        self.__most_recent = self.__emails[0]

        self.__email_event = Event()
        self.__email_event += handler

    def __get_emails(self):
        """Gets a list of all the emails that have been recieved

        Returns: 
            a list containing dictionaries of the form {idNumber, threadNumber} 
            that represent all messages recieved by a class
        """
        # This returns a list of Gmail message objects. Documentation can be found at
        # https://developers.google.com/gmail/api/v1/reference/users/messages/list
        return self.__service.users().messages().list(userId='me').execute()['messages']

    def run(self):
        """Watch the gmail inbox for commands
        """
        most_recent = self.__most_recent
        while True:
            emails = self.__get_emails()

            if most_recent != emails[0]:
                print("new messsage recieved")

                # Dispatch event for new email
                self.__email_event()

                # Reset most recent
                most_recent = emails[0]

            else:
                time.sleep(0.3)
