import password_generator
from email_handler.email import Email_Handler


class Controller:
    def __init__(self, recipients, password):
        self.__source = 'Controller: '

        self.__email_handler = Email_Handler(
            recipients, self.handle_new_email)
        self.__password = password

    def get_password(self):
        """Get the current password

        Returns: The current Password
        """
        return self.__password

    def new_password(self):
        """Creates a new password

        Returns: A new password
        """
        # create new password
        return password_generator.create_password()
        # have password reset

    def handle_new_email(self):
        """Handles a new email event
        """
        print(self.__source)
        # TODO: flush out to respond to various calls

        # get emails
        email = self.__email_handler.get_most_recent_email()
        # use content of email to decide on next action
        message = self.__email_handler.get_email_body(email['id'])
        print(message)

    # TODO: May not need this function with new event architecture

    def run(self):
        """Waits for messages from other components of the app and dispatches 
        commands as necessary
        """
        # waits for new messages and reacts based on message
        print("Watch")
