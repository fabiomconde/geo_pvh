import requests

GEOSERVER_URL = "http://localhost:8080/geoserver/rest"
USER = "admin"
PASSWORD = "geoserver"
WORKSPACE = "geo"
DATASTORE = "pvh_store"

def init_geoserver():
    # 1. Create Workspace
    print(f"Checking Workspace {WORKSPACE}...")
    resp = requests.get(f"{GEOSERVER_URL}/workspaces/{WORKSPACE}", auth=(USER, PASSWORD))
    if resp.status_code == 404:
        print(f"Creating Workspace {WORKSPACE}...")
        data = f"<workspace><name>{WORKSPACE}</name></workspace>"
        headers = {"Content-Type": "application/xml"}
        r = requests.post(f"{GEOSERVER_URL}/workspaces", auth=(USER, PASSWORD), headers=headers, data=data)
        print(f"Create Workspace: {r.status_code}")
    else:
        print(f"Workspace {WORKSPACE} exists.")

    # 2. Create/Update PostGIS Datastore with Schema 'geo'
    print(f"Configuring Datastore {DATASTORE}...")
    
    # XML payload
    data = f"""
    <dataStore>
      <name>{DATASTORE}</name>
      <connectionParameters>
        <entry key="host">db</entry>
        <entry key="port">5432</entry>
        <entry key="database">pvh_geoportal</entry>
        <entry key="user">postgres</entry>
        <entry key="passwd">postgres</entry>
        <entry key="dbtype">postgis</entry>
        <entry key="schema">geo</entry> <!-- Explicitly set schema -->
      </connectionParameters>
    </dataStore>
    """
    headers = {"Content-Type": "application/xml"}

    # Check if exists
    resp = requests.get(f"{GEOSERVER_URL}/workspaces/{WORKSPACE}/datastores/{DATASTORE}", auth=(USER, PASSWORD))
    if resp.status_code == 404:
        print(f"Creating Datastore {DATASTORE}...")
        r = requests.post(f"{GEOSERVER_URL}/workspaces/{WORKSPACE}/datastores", auth=(USER, PASSWORD), headers=headers, data=data)
    else:
        print(f"Updating Datastore {DATASTORE} to ensure schema=geo...")
        r = requests.put(f"{GEOSERVER_URL}/workspaces/{WORKSPACE}/datastores/{DATASTORE}", auth=(USER, PASSWORD), headers=headers, data=data)
    
    print(f"Datastore Result: {r.status_code}")
    if r.status_code >= 400:
        print(r.text)

if __name__ == "__main__":
    init_geoserver()
