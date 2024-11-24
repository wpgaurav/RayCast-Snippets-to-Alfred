import json
import os
import uuid
import zipfile

def convert_json_to_alfred_snippets(input_file_path, output_dir, zip_file_path):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Load the input JSON data
    with open(input_file_path, "r") as infile:
        snippets = json.load(infile)

    # Convert each snippet into Alfred format and save them as individual files
    for snippet in snippets:
        alfred_snippet = {
            "alfredsnippet": {
                "snippet": snippet["text"],
                "uid": str(uuid.uuid4()),
                "name": snippet["name"],
                "keyword": snippet.get("keyword", "")
            }
        }
        # Save each snippet as a separate JSON file
        output_file_path = os.path.join(output_dir, f"{snippet['name']}.json")
        with open(output_file_path, "w") as outfile:
            json.dump(alfred_snippet, outfile, indent=2)

    # Create a zip file containing all the snippet files
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        for root, _, files in os.walk(output_dir):
            for file in files:
                zipf.write(
                    os.path.join(root, file),
                    os.path.relpath(os.path.join(root, file), output_dir)
                )

# Paths for input JSON, output directory, and the resulting zip file
input_file_path = "input.json"  # Replace with the actual path to your input JSON file
output_dir = "alfred_snippets"  # Replace with the desired output directory
zip_file_path = "alfred_snippets.zip"  # Replace with the desired zip file path

# Call the function
convert_json_to_alfred_snippets(input_file_path, output_dir, zip_file_path)

print(f"Alfred snippets have been saved and zipped at: {zip_file_path}")
