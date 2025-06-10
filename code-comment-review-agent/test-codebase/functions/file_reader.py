def read_file(file_path):
    """Read the contents of a file and return as a string.

    Args:
        file_path (str): Path to the file to be read.

    Returns:
        str: Contents of the file if successful, otherwise an error message.
             Possible return values:
             - File contents (success)
             - "File not found!" (FileNotFoundError)
             - "Permission denied!" (PermissionError)
             - Generic error message (other exceptions)
    """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "File not found!"
    except PermissionError:
        return "Permission denied!"
    except Exception as e:
        return f"An error occurred: {str(e)}"