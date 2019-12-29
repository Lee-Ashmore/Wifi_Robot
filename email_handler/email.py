import base64
import email
import os.path
import pickle
import time
from email.mime.text import MIMEText

from apiclient import errors
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from .credentials import Credentials
from .watcher import Watcher


class Email_Handler:
    """ A class that will handle all interactions with gmail
    """

    def __init__(self, recipients, handlers):
        self.__source = 'Email_handler: '

        self.__recipients = recipients
        self.__user_id = 'Wifi.Robot.Overlord@gmail.com'

        self.__creds = Credentials()
        self.__service = self.__creds.get_service()

        self.__watcher = Watcher(self.__service, handlers)

    def __create_message(self, to, subject, message_text):
        """Create a message for an email.

        Args:
            sender: Email address of the sender.
            to: Email address of the receiver.
            subject: The subject of the email message.
            message_text: The text of the email message.

        Returns:
            An object containing a base64url encoded email object.
        """
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = self.__user_id
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

    def __get_emails(self):
        """Gets a list of all the emails that have been recieved
        """
        # This returns a list of Gmail message objects. Documentation can be found at
        # https://developers.google.com/gmail/api/v1/reference/users/messages/list
        return self.__service.users().messages().list(userId='me').execute()['messages']

    def __send_message(self, message):
        """Send a message through Gmail

        Args:
            message: base64 encoded message

        Returns: 
            The message entity returned by the Gmail api
        """
        try:
            message = (self.__service.users().messages().send(
                userId=self.__user_id, body=message).execute())
            print(f'{self.__source}Message Id: %s' % message['id'])
            return message
        except errors.HttpError as e:
            print(f'{self.__source}An error has occured: %s' % e)

    def get_most_recent_email(self):
        """Gets the most recent email in the inbox

        Returns: 
            A gmail Resource object representing an email
        """
        return self.__get_emails()[0]

    def get_email_body(self, message_id):
        """Gets the text from an email

        Args: 
            message_id: the Gmail id of the message you want to get the text from

        Returns:
            A string containing the text from the body of the message
        """
        try:
            message = self.__service.users().messages().get(
                userId='me', id=message_id, format='raw').execute()

            message_string = base64.urlsafe_b64decode(
                message['raw'].encode('ASCII')).decode()

            # TODO: Find a cleaner/Pythonic way to do this. Looks like garbage atm
            text = email.message_from_string(
                message_string).get_payload(i=0).get_payload()
        except Exception:
            time.sleep(1)

            # HOLY SHIT THIS IS A BAD IDEA. NEVER GETTING THROUGH REVIEW ============================
            message = self.__service.users().messages().get(
                userId='me', id=message_id, format='raw').execute()

            message_string = base64.urlsafe_b64decode(
                message['raw'].encode('ASCII')).decode()

            text = email.message_from_string(
                message_string).get_payload(i=0).get_payload()
            # I guess it works... ====================================================================
        return text

    def send(self, message_text):
        """Sends a given message to all of the recipients in the classes 
        recipients variable

        Args:
            message_text: The text of the message to be sent

        Returns: 
            A string id of the message that was sent
        """
        for recipient in self.__recipients:
            message = self.__create_message(recipient, "Wifi", message_text)
            return self.__send_message(message)
