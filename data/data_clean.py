import json

# Input and output file paths
input_file_path = "geotis_clean.json"
output_file_path = "geotis_filtered.json"

# Function to filter out entries with "Thermalbad / Balneologie" in the "use" field
def filter_thermalbad(data):
    if "features" in data:
        # Retain only those features that do not have "Thermalbad / Balneologie" in "use"
        data["features"] = [
            feature for feature in data["features"]
            if "Thermalbad / Balneologie" not in feature.get("properties", {}).get("use", [])
        ]
    return data

def filter_trinkwasser(data):
    if "features" in data:
        # Retain only those features that do not have "Thermalbad / Balneologie" in "use"
        data["features"] = [
            feature for feature in data["features"]
            if "Trink- / Brauchwasser" not in feature.get("properties", {}).get("use", [])
        ]
    return data

def filter_ungenutzt(data):
    if "features" in data:
        # Retain only those features that do not have "Thermalbad / Balneologie" in "use"
        data["features"] = [
            feature for feature in data["features"]
            if "ungenutzt" not in feature.get("properties", {}).get("use", [])
        ]
    return data

# Load, filter, and save the JSON data
with open(input_file_path, "r", encoding="utf-8") as infile, \
     open(output_file_path, "w", encoding="utf-8") as outfile:
    # Load the JSON content
    data = json.load(infile)

    # Filter the entries
    filtered_data = filter_thermalbad(data)
     # Filter the entries
    filtered_data = filter_trinkwasser(filtered_data)
    filtered_data = filter_ungenutzt(filtered_data)

    # Write the filtered data back to the output file
    json.dump(filtered_data, outfile, ensure_ascii=False, indent=4)
