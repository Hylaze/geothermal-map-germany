import json
import pyproj


# Function to clean and convert coordinate strings to float
def clean_coordinate(value_str):
    try:
        # Remove any unwanted characters such as non-breaking spaces, "m", and "."
        cleaned_value = value_str.replace("\xa0", "").replace("m", "").replace('.', '').strip()
       
        formatted_number = round(float(cleaned_value) / 1000000, 2)  # Divide by 1 million to get 3.29

        return float(cleaned_value)
    except ValueError as e:
        print(f"Error converting '{value_str}' to float: {e}")
        raise

gauss_kruger = pyproj.CRS("EPSG:31467")  # This is for Zone 3

# Define the WGS84 Projection (Latitude/Longitude)
wgs84 = pyproj.CRS("EPSG:4326")  # WGS84 (lat, lon)

# Create a Transformer to convert from Gauss-Krüger to WGS84
transformer = pyproj.Transformer.from_crs(gauss_kruger, wgs84, always_xy=True)

def convert_gauss_krueger_to_wgs84(right_value, high_value):
    """Convert Gauss-Krüger (X, Y) coordinates to WGS84 (longitude, latitude)."""
    longitude, latitude = transformer.transform(right_value, high_value)
    return latitude, longitude


# Function to convert a single entry
def convert_entry(entry):
    # Use the clean_coordinate function to handle coordinates
    right_value = clean_coordinate(entry["location"]["coordinates"]["right_value"])
    high_value = clean_coordinate(entry["location"]["coordinates"]["high_value"])
   
    latitude, longitude = convert_gauss_krueger_to_wgs84(right_value, high_value)

    # Build the output data structure for a single entry
    converted_entry = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [longitude, latitude]
        },
        "properties": {
            "use": [entry["usage"]["main"]],
            "state": entry["status"],
            "title": entry["name"],
            "attributes": [],
            "details": {
                "Ptherm": f"{entry['thermal_data']['installed_capacity']['total']} MW",
                "Pel": "0 MW",  # Assuming no electric capacity is available
                "Tmax": entry["thermal_data"]["temperature"],
                "Teufe": entry["thermal_data"]["depth"],
                "Förderrate": entry["thermal_data"]["flow_rate"],
                "Inbetriebnahme": "kein Eintrag"  # Assuming missing commissioning date
            }
        }
    }

    return converted_entry

# Function to process the entire input file and save to output file
def process_json(input_filepath, output_filepath):
    # Read input JSON data
    with open(input_filepath, 'r', encoding='utf-8') as infile:
        input_data = json.load(infile)
    
    # Process each entry in "thermal_springs"
    features = [convert_entry(entry) for entry in input_data["thermal_springs"]]
    
    # Create the output data structure
    output_data = {
        "type": "FeatureCollection",
        "features": features
    }
    
    # Write the output JSON data to file
    with open(output_filepath, 'w', encoding='utf-8') as outfile:
        json.dump(output_data, outfile, indent=4)
    print(f"Converted data has been saved to {output_filepath}")

# Specify the input and output file paths
input_file = 'anlagen_daten.json'   # Path to your input file

output_file = 'anlagen_clean.json' # Path to your output file

# Run the conversion
process_json(input_file, output_file)
