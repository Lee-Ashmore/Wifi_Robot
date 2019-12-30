from controller import Controller
from password_generator import create_password


if __name__ == "__main__":
    new_password = create_password()

    # Use screen scraper to change password

    test = Controller(["wifi.robot.overlord@gmail.com"], 'test_password')
    test.run()

    # Email_Handler = Email_Handler(["wifi.robot.overlord@gmail.com"])
    # Email_Handler.send("Your new password is: " + new_password)

# TODO: create main program flow and lifecycle here
