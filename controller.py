import password_generator
from email_handler.email import Email_Handler


class Controller:
    def __init__(self, recipients, password):
        self.__source = '\nController: '
        self.__password = password
        self.__recipients = recipients

        self.__email_handler = Email_Handler(
            self.__recipients, self.handle_new_email)

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
        email = self.__email_handler.get_most_recent_email()
        message = self.__email_handler.get_email_body(email['id'])
        sender = self.__email_handler.get_email_sender(email['id'])

        if 'COMMAND' in message:

            if 'test' in message:
                print(f'{self.__source} Test Command Recieved')

            if 'new password' in message:
                print(f'{self.__source} New Password Command Recieved')
                # create new password
                # store new password
                # reset current password via screenscraper
                # notify users of change
                self.__email_handler.send(
                    f'Password has been reset: {self.__password}')

            if 'get password' in message:
                print(f'{self.__source} Get Password Command Recieved')
                self.__email_handler.send('test', recipients=[sender])

            if 'add user' in message:
                print(f'{self.__source} Add User Command Recieved')
                self.__recipients.append(sender)
                # send email with message explaing email use

            if 'help' in message:
                print(f'{self.__source} Help Command Recieved')
                # send email with message explaing email use

    def run(self):
        """Waits for messages from other components of the app and dispatches 
        commands as necessary
        """

        # waits for new messages and reacts based on message
        try:
            self.__email_handler.run()
        except KeyboardInterrupt:
            print('\nClosing...\n')
        except Exception as e:
            print(f'{self.__source}: and error has occured: %s' % e)
