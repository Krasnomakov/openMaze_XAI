import json

def convert_to_json(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            tokens = content.split()

            # Create a dictionary or list object
            data = {
                'tokens': tokens
            }

            # Convert the Python object to JSON
            json_data = json.dumps(data, indent=4)
            return json_data
    except FileNotFoundError:
        print("File not found.")
    except IOError:
        print("Error reading the file.")

# Provide the path to your text file
file_path = 'user 0.txt'

# Call the function to convert to JSON
json_data = convert_to_json(file_path)
print(json_data)

