import requests
import sys

GEOSERVER_URL = "http://localhost:8080/geoserver/rest"
USER = "admin"
PASSWORD = "geoserver"
WORKSPACE = "geo"
DATASTORE = "pvh_store"
LAYER_NAME = "distritos_pvh"

def publish_layer():
    # Check if Exists first
    url_check = f"{GEOSERVER_URL}/workspaces/{WORKSPACE}/datastores/{DATASTORE}/featuretypes/{LAYER_NAME}"
    resp = requests.get(url_check, auth=(USER, PASSWORD))
    if resp.status_code == 200:
        print(f"Layer {LAYER_NAME} already exists.")
        return

    # Create FeatureType (Layer) with specific XML structure
    url = f"{GEOSERVER_URL}/workspaces/{WORKSPACE}/datastores/{DATASTORE}/featuretypes"
    headers = {"Content-Type": "application/xml"}
    
    # Minimal clean XML
    # Try nativeName matching the table name exactly (case sensitive?). Table is distritos_pvh.
    data = f"""<featureType>
  <name>{LAYER_NAME}</name>
  <nativeName>{LAYER_NAME}</nativeName>
  <title>Distritos de Porto Velho</title>
  <srs>EPSG:4326</srs>
  <enabled>true</enabled>
</featureType>"""
    
    print(f"Publishing layer {LAYER_NAME}...")
    # print(data)
    response = requests.post(url, auth=(USER, PASSWORD), headers=headers, data=data)
    
    if response.status_code == 201:
        print("Layer published successfully.")
    else:
        print(f"Failed to publish layer: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    try:
        publish_layer()
    except Exception as e:
        print(f"Error: {e}")
