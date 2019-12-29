import string
import random


def create_password(length=10):
    """creates a random string of a given length with a default length of 10.

    Args:
        length: The desired length of the string to be generated.

    Returns:
        A randomly generated string of the given length.
    """
    characters = string.ascii_letters + string.digits

    return ''.join(random.choice(characters) for i in range(length))
