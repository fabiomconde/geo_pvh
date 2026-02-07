import requests
import json

# IBGE V2 API
# resolucao=5 -> Distrito
url = "https://servicodados.ibge.gov.br/api/v2/malhas/11?formato=application/vnd.geo+json&resolucao=5&qualidade=minima"

print(f"Fetching {url}...")
try:
    resp = requests.get(url)
    data = resp.json()
    
    if data.get('type') == 'FeatureCollection':
        features = data.get('features', [])
        print(f"Total features: {len(features)}")
        
        count_pvh = 0
        print("\nListing features:")
        for f in features:
            props = f.get('properties', {})
            code = props.get('codarea')
            name = props.get('name') # Usually it doesn't have name in properties for v2, just code
            
            # If name is missing, we only have code
            print(f"Code: {code}")
            
            if str(code).startswith('1100205'):
                count_pvh += 1
                print(f"  -> MATCH PORTO VELHO: {code}")
                
        print(f"\nTotal matches for 1100205: {count_pvh}")

    else:
        print("Not a FeatureCollection")
        print(data.keys())

except Exception as e:
    print(f"Error: {e}")
