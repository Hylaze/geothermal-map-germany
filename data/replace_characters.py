import json

# Replacement map for fixing Unicode issues
replacement_map = {
    "\u00b0": "°",
    "\u00f6": "ö",
    # Add more replacements as needed
}

# Function to replace unwanted Unicode characters in a string
def replace_unwanted_chars(value):
    if isinstance(value, str):  # Only process string values
        for old, new in replacement_map.items():
            value = value.replace(old, new)
    return value

# Read the input file and write the processed content to an output file
input_file_path = "geotis.json"
output_file_path = "geotis_clean.json"

with open(input_file_path, "r", encoding="utf-8") as infile, \
     open(output_file_path, "w", encoding="utf-8") as outfile:
    # Read file content and decode the JSON
    file_content = infile.read()  # Read the entire file content as a string
    parsed_data = json.loads(file_content)  # Parse the JSON content into a dictionary

    # Process the parsed JSON dictionary
    processed_data = {
        key: replace_unwanted_chars(value) for key, value in parsed_data.items()
    }

    # Write the cleaned JSON back to the output file
    outfile.write(json.dumps(processed_data, ensure_ascii=False, indent=4))
