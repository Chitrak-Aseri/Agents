import re

def is_palindrome(s):
    """
    Check if a string is a palindrome (reads the same forwards and backwards).

    Args:
        s (str): The input string to check.

    Returns:
        bool: True if the string is a palindrome after removing non-alphanumeric 
              characters and converting to lowercase, False otherwise.
    """
    cleaned_string = re.sub(r'[^a-zA-Z0-9]', '', s).lower()  # Remove non-alphanumeric chars and lowercase
    return cleaned_string == cleaned_string[::-1]