import requests
import json

url = "https://servicodados.ibge.gov.br/api/v2/malhas/11?formato=application/vnd.geo+json&resolucao=5&qualidade=minima"
print(f"Testing {url}")
resp = requests.get(url)
data = resp.json()

if 'features' in data:
    for f in data['features']:
        code = str(f['properties'].get('codarea', ''))
        if code.startswith('1100205'):
             print(f"Found PVH Feature: {code}")
             print(f"Props: {f['properties']}")
