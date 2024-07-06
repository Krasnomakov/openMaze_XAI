def count_tokens(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            tokens = content.split()
            return len(tokens)
    except FileNotFoundError:
        print("File not found.")
    except IOError:
        print("Error reading the file.")

# Provide the path to your text file
file_path = 'user 0.txt'

# Call the function to count tokens
num_tokens = count_tokens(file_path)
print("Number of tokens:", num_tokens)
