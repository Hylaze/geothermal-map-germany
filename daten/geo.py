import geopandas as gpd

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
germany = world[world['name'] == 'Germany']
germany.to_file("germany.geojson", driver='GeoJSON')