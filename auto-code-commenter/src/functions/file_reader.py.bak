def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "File not found!"
    except PermissionError:
        return "Permission denied!"
    except Exception as e:
        return f"An error occurred: {str(e)}"
