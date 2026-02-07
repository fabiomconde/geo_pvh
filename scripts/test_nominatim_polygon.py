import requests
import json

def get_polygon(query):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': query,
        'format': 'json',
        'limit': 1,
        'polygon_geojson': 1
    }
    headers = {
        'User-Agent': 'PVH_GeoPortal_Dev_Polygon_Test'
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        if data:
            layout = data[0]
            print(f"Name: {layout.get('display_name')}")
            print(f"OSM Type: {layout.get('osm_type')}")
            print(f"GeoJSON Type: {layout.get('geojson', {}).get('type')}")
            return layout
        else:
            print("No data found.")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

print("Testing Abunã...")
get_polygon("Distrito de Abunã, Porto Velho, Rondônia, Brazil")

print("\nTesting Jaci-Paraná...")
get_polygon("Distrito de Jaci-Paraná, Porto Velho, Rondônia, Brazil")
