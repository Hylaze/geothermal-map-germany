import csv
import json


# Sample GeoJSON data
geojson_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [10.1, 51.1]
            },
            "properties": {
                "use": ["wärme", "Strom"],
                "state": "in Betrieb",
                "title": "Name der Anlage",
                "attributes": ["Sonde", "Hydrogeothermie", "Forschung", "Aquiferspeicher", "Grubenwasser", "Geschlossenes tiefengeothermisches System"],
                "details": [
                    {
                        "Ptherm": "thermische Leistung",
                        "Pel": "elektrische Leistung",
                        "Tmax": "maximale Thermalwassertemperatur",
                        "Teufe": "senkrechte Tiefe der Bohrung",
                        "Förderrate": "leer",
                        "Inbetriebnahme": "2001"
                    }
                ]
            }
        },
        # Additional features...
    ]
}

# Unique columns for use and attributes based on input data
USE_COLUMNS = ["wärme", "Strom", "Forschung"]
ATTRIBUTE_COLUMNS = ["Sonde", "Hydrogeothermie", "Forschung", "Aquiferspeicher", "Grubenwasser", "Geschlossenes tiefengeothermisches System"]

# Convert GeoJSON to CSV
def geojson_to_csv(geojson_data, csv_filename="output.csv"):
    headers = [
        "latitude", "longitude", "state", "title",
        "Ptherm", "Pel", "Tmax", "Teufe", "Förderrate", "Inbetriebnahme"
    ] + USE_COLUMNS + ATTRIBUTE_COLUMNS
    
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        
        for feature in geojson_data["features"]:
            row = {}
            
            # Coordinates
            row["latitude"], row["longitude"] = feature["geometry"]["coordinates"]
            
            # Properties
            properties = feature["properties"]
            row["state"] = properties.get("state", "")
            row["title"] = properties.get("title", "")
            
            # Set use columns
            use = set(properties.get("use", []))
            for use_col in USE_COLUMNS:
                row[use_col] = 1 if use_col in use else 0

            # Set attributes columns
            attributes = set(properties.get("attributes", []))
            for attr_col in ATTRIBUTE_COLUMNS:
                row[attr_col] = 1 if attr_col in attributes else 0
            
            # Set details
            details = properties.get("details", [{}])[0]
            row["Ptherm"] = details.get("Ptherm", "")
            row["Pel"] = details.get("Pel", "")
            row["Tmax"] = details.get("Tmax", "")
            row["Teufe"] = details.get("Teufe", "")
            row["Förderrate"] = details.get("Förderrate", "")
            row["Inbetriebnahme"] = details.get("Inbetriebnahme", "")
            
            writer.writerow(row)

# Run the function to convert and save as CSV
# geojson_to_csv(geojson_data)

# Convert CSV back to GeoJSON
def csv_to_geojson(csv_filename="output.csv", geojson_filename="output.geojson"):
    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }
    
    with open(csv_filename, mode="r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        
        for row in reader:
            # Coordinates
            latitude = float(row["latitude"])
            longitude = float(row["longitude"])
            
            # Reassemble use list based on columns
            use = [col for col in USE_COLUMNS if row[col] == "1"]
            
            # Reassemble attributes list based on columns
            attributes = [col for col in ATTRIBUTE_COLUMNS if row[col] == "1"]
            
            # Extract details
            details = {
                "Ptherm": row["Ptherm"],
                "Pel": row["Pel"],
                "Tmax": row["Tmax"],
                "Teufe": row["Teufe"],
                "Förderrate": row["Förderrate"],
                "Inbetriebnahme": row["Inbetriebnahme"]
            }
            
            # Create feature structure
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [longitude, latitude]
                },
                "properties": {
                    "use": use,
                    "state": row["state"],
                    "title": row["title"],
                    "attributes": attributes,
                    "details": [details]
                }
            }
            
            geojson_data["features"].append(feature)
    
    # Write to a GeoJSON file
    with open(geojson_filename, mode="w", encoding="utf-8") as geojson_file:
        json.dump(geojson_data, geojson_file, indent=2, ensure_ascii=False)

# Run the function to convert CSV back to GeoJSON
csv_to_geojson()
