import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import json


def to_geojson_geopandas(input_csv: str, output_geojson: str) -> None:
    """
    Converts geothermal project data from CSV to GeoJSON using GeoPandas.
    
    Parameters:
        input_csv (str): Path to the input CSV file.
        output_geojson (str): Path to the output GeoJSON file.
    """
    # Load CSV data
    df = pd.read_csv(input_csv, delimiter=';')

    # Drop rows with missing coordinates or status
    df = df.dropna(subset=['Koordinaten', 'Status', 'Name auf der Karte'])

    # Parse coordinates into Point geometries
    def parse_point(coord_str):
        try:
            lat_str, lon_str = coord_str.split(',')
            lat = float(lat_str.strip())
            lon = float(lon_str.strip())
            return Point(lon, lat)  # GeoJSON expects [lon, lat]
        except (ValueError, IndexError):
            return None

    df['geometry'] = df['Koordinaten'].apply(parse_point)
    df = df.dropna(subset=['geometry'])

    # Build properties dictionary
    def build_properties(row):
        return {
            "use": [row['Art der Nutzung']] if pd.notna(row['Art der Nutzung']) else [],
            "state": row['Status'] if not str(row['Status']).startswith('A') else [row.get('Output', 'kein Eintrag')],
            "title": row.get('Name auf der Karte', 'kein Titel'),
            "attributes": [],
            "details": {
                "Ptherm": f"{row['Mwtherm (installierte Leistung geothermisch)']} MW"
                          if pd.notna(row['Mwtherm (installierte Leistung geothermisch)']) else "kein Eintrag",
                "Pel": f"{row['MWel']} MW" if pd.notna(row['MWel']) else "kein Eintrag",
                "Tmax": f"{row['max. Temperatur in °C']} °C" if pd.notna(row['max. Temperatur in °C']) else "kein Eintrag",
                "Teufe": f"{row['Teufe in m (TVD)']} m" if pd.notna(row['Teufe in m (TVD)']) else "kein Eintrag",
                "Förderrate": f"{row['Förderrate (l/s) (maximal)']} l/s"
                              if pd.notna(row['Förderrate (l/s) (maximal)']) else "kein Eintrag",
                "Inbetriebnahme": row['Jahr d. Inbetrieb-nahme']
                                  if pd.notna(row['Jahr d. Inbetrieb-nahme']) else "kein Eintrag",
                "Link zum Lexikon": f"{row['Lexikon']}"
                                     if pd.notna(row['Lexikon']) else "kein Eintrag",
            }
        }

    df['properties'] = df.apply(build_properties, axis=1)

    # Create the GeoDataFrame with specified CRS (WGS84)
    gdf = gpd.GeoDataFrame(df[['properties', 'geometry']], geometry='geometry', crs="EPSG:4326")

    # Prepare for GeoJSON output
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    # Iterate through GeoDataFrame and convert each row to a feature
    for _, row in gdf.iterrows():
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row['geometry'].x, row['geometry'].y]
            },
            "properties": row['properties']
        }
        geojson["features"].append(feature)

    # Write to GeoJSON file
    with open(output_geojson, 'w', encoding='utf-8') as f:
        json.dump(geojson, f, ensure_ascii=False, indent=4)

    print(f"GeoJSON successfully created at: {output_geojson}")


# Example usage:
input_file = 'daten/Projektliste Tiefe Geothermie_2025_intern_13.05_neu.CSV'
output_file = 'anlagen_neu_4.json'
to_geojson_geopandas(input_file, output_file)
