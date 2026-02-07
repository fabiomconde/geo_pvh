import requests
import json

# Try fetching State 11 (RO) divided by districts
url = "https://servicodados.ibge.gov.br/api/v3/malhas/estados/11?formato=application/vnd.geo+json&qualidade=minima&divisao=distrito"
print(f"Testing {url}")
resp = requests.get(url)
print(f"Status: {resp.status_code}")
try:
    data = resp.json()
    if 'features' in data:
        print(f"Features: {len(data['features'])}")
        print("First feature props:", data['features'][0]['properties'])
        
        # Check if any feature is from PVH
        pvh_count = 0
        for f in data['features']:
            if str(f['properties'].get('codarea', '')).startswith('1100205'):
                pvh_count += 1
        print(f"PVH Districts found: {pvh_count}")
        
    else:
        print("No features key")
except Exception as e:
    print(f"JSON Error: {e}")
    print(resp.text[:200])
