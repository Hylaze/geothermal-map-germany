
from pyproj import Proj, Transformer

# Define the UTM Zone 32N projection (used for Rechtswert and Hochwert in the example)
utm_zone_32n = Proj(proj='utm', zone=32, ellps='WGS84', preserve_units=False)

# Alternatively, use pyproj.Transformer for a more modern approach
transformer = Transformer.from_crs("epsg:32632", "epsg:4326", always_xy=True)

# Input UTM coordinates (Rechtswert, Hochwert)
utm_coords = [
    (328411.13, 5690671.37),
    (348074, 5691579),
    (3436000, 5450000),
    (3690507, 5334086),
    (3697685, 5342910),
    (3697700, 5343000),
    (3697784, 5350469),
    (3703494, 5340571)
]

# Convert UTM to latitude and longitude
latlon_coords = []
for x, y in utm_coords:
    lon, lat = transformer.transform(x, y)
    latlon_coords.append((lat, lon))

# Print the converted coordinates
for lat, lon in latlon_coords:
    print(f"{lat}, {lon}")
