import requests
import json

url = "https://servicodados.ibge.gov.br/api/v3/malhas/municipios/1100205?formato=application/vnd.geo+json&qualidade=intermediaria&divisao=distrito"
response = requests.get(url)
data = response.json()

if 'features' in data:
    print(f"Feature count: {len(data['features'])}")
    for i, f in enumerate(data['features']):
        print(f"Feature {i} properties: {f['properties']}")
else:
    print("No features found or invalid structure")
