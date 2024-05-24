# import yaml

def load_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def save_file(data, file_path):
    with open(file_path, 'w') as file:
        file.write(data)

def replace_strings(data, replacements):
    if isinstance(data, dict):
        return {k: replace_strings(v, replacements) for k, v in data.items()}
    elif isinstance(data, list):
        return [replace_strings(item, replacements) for item in data]
    elif isinstance(data, str):
        for old_string, new_string in replacements.items():
            data = data.replace(old_string, new_string)
        return data
    else:
        return data
        return data

if __name__ == "__main__":
    input_file = 'vitae.yml'
    output_file = 'vitae.yml'
    replacements = {"‘Anthony’": "'Anthony'", 
                    "`Anthony’": "'Anthony'", 
                    "Xiang Anthony Chen": "Xiang 'Anthony' Chen",
                    "Xiang'Anthony'": "Xiang 'Anthony'"}  # Replace 'a' with 'e' and 'o' with 'u'
    
    data = load_file(input_file)
    modified_data = replace_strings(data, replacements)
    save_file(modified_data, output_file)
    print(f"Modified file saved as {output_file}")
