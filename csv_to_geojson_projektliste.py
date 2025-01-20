import csv
import json

def csv_to_geojson(input_csv, output_geojson):
    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }

    with open(input_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')

        for row in reader:
            # Extract coordinates and ensure they are valid
            try:
                coords = row['Koordinaten'].split(',')
                longitude = float(coords[1].strip())
                latitude = float(coords[0].strip())
            except (IndexError, ValueError):
                continue  # Skip rows with invalid coordinates

            # Build the feature properties
            properties = {
                "use": [row['Art der Nutzung']] if row['Art der Nutzung'] else [],
                "state": row['Status'] if not row['Status'].startswith('A') else [row['Output']],
                "title": row['Name'],
                "attributes": [],
                "details": {
                    "Ptherm": f"{row['Mwtherm (installierte Leistung geothermisch)']} MW" if row['Mwtherm (installierte Leistung geothermisch)'] else "kein Eintrag",
                    "Pel": f"{row['MWel']} MW" if row['MWel'] else "kein Eintrag",
                    "Tmax": f"{row['max. Temperatur']} °C" if row['max. Temperatur'] else "kein Eintrag",
                    "Teufe": f"{row['Teufe in m (TVD)']} m" if row['Teufe in m (TVD)'] else "kein Eintrag",
                    "Förderrate": f"{row['Forderrate (l/s) (maximal)']} l/s" if row['Forderrate (l/s) (maximal)'] else "kein Eintrag",
                    "Inbetriebnahme": row['Jahr d. Inbetrieb-nahme'] if row['Jahr d. Inbetrieb-nahme'] else "kein Eintrag"
                }
            }

            # Build the feature
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [longitude, latitude]
                },
                "properties": properties
            }

            # Add the feature to the GeoJSON data
            geojson_data["features"].append(feature)

    # Write the GeoJSON data to the output file
    with open(output_geojson, 'w', encoding='utf-8') as geojsonfile:
        json.dump(geojson_data, geojsonfile, ensure_ascii=False, indent=4)

# Example usage:
input_csv = 'projektliste_dw3.csv'  # Replace with your input CSV file path
output_geojson = 'anlagen_projektliste3.json'  # Replace with your desired GeoJSON output file path
csv_to_geojson(input_csv, output_geojson)
