import re

def is_palindrome(s):
    cleaned_string = re.sub(r'[^a-zA-Z0-9]', '', s).lower()
    return cleaned_string == cleaned_string[::-1]
