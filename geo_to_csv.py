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
geojson_to_csv(geojson_data)
