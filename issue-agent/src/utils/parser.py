import os
import xmltodict

def parse_all_documents(folder_path):
    combined_content = ""
    for file in os.listdir(folder_path):
        path = os.path.join(folder_path, file)
        if file.endswith(".xml"):
            with open(path) as f:
                doc = xmltodict.parse(f.read())
                combined_content += str(doc)
        elif file.endswith(".json"):
            with open(path) as f:
                combined_content += f.read()
        elif file.endswith(".txt"):
            with open(path) as f:
                combined_content += f.read()
        # Add other formats as needed
    return combined_content