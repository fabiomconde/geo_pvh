import requests
import json
import os
import time

# User Data
DISTRITOS_DATA = {
    "Porto Velho": {
        "populacao": "460.434",
        "distancia_sede": "0 km",
        "caracteristicas": "Área urbana central, sede do poder público, comércio e serviços"
    },
    "Abunã": {
        "populacao": "2.385",
        "distancia_sede": "180 km",
        "caracteristicas": "Distrito às margens do Rio Madeira, comunidade tradicional, pesca artesanal"
    },
    "Calama": {
        "populacao": "2.312",
        "distancia_sede": "250 km",
        "caracteristicas": "Distrito ribeirinho, acesso fluvial, economia extrativista"
    },
    "Demarcação": { 
        "populacao": "845",
        "distancia_sede": "300 km",
        "caracteristicas": "Distrito com presença de comunidades quilombolas"
    },
    "Extrema": {
        "populacao": "7.171",
        "distancia_sede": "210 km",
        "caracteristicas": "Distrito fronteiriço, agricultura familiar"
    },
    "Fortaleza do Abunã": {
        "populacao": "474",
        "distancia_sede": "190 km",
        "caracteristicas": "Distrito com forte presença de assentamentos rurais"
    },
    "Jaci-Paraná": { 
        "populacao": "11.671",
        "distancia_sede": "100 km",
        "caracteristicas": "Distrito com conflitos fundiários, pecuária"
    },
    "Mutum-Paraná": { 
        "populacao": "7.509",
        "distancia_sede": "150 km",
        "caracteristicas": "Distrito com comunidades ribeirinhas, pesca"
    },
    "Nazaré": {
        "populacao": "607",
        "distancia_sede": "140 km",
        "caracteristicas": "Distrito com comunidades tradicionais"
    },
    "Nova Califórnia": {
        "populacao": "5.216",
        "distancia_sede": "280 km",
        "caracteristicas": "Distrito com projetos de assentamento"
    },
    "São Carlos": {
        "populacao": "1.171",
        "distancia_sede": "130 km",
        "caracteristicas": "Distrito com presença indígena"
    },
    "Vista Alegre do Abunã": {
        "populacao": "8.260",
        "distancia_sede": "170 km",
        "caracteristicas": "Distrito agrícola, produção familiar"
    },
     "Rio Pardo": { 
        "populacao": "800",
        "distancia_sede": "320 km",
        "caracteristicas": "Comunidade rural, agricultura familiar, acesso fluvial e terrestre"
    },
}

def get_coordinates(query):
    # Nominatim API
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': query,
        'format': 'json',
        'limit': 1
    }
    headers = {
        'User-Agent': 'PVH_GeoPortal_Dev_Script' # Required by Nominatim
    }
    
    try:
        resp = requests.get(url, params=params, headers=headers)
        data = resp.json()
        if data and len(data) > 0:
            return float(data[0]['lon']), float(data[0]['lat'])
    except Exception as e:
        print(f"Error fetching {query}: {e}")
    return None, None

def main():
    features = []
    
    print(f"Fetching coordinates for {len(DISTRITOS_DATA)} districts...")
    
    for name, info in DISTRITOS_DATA.items():
        # Construct Query
        query = ""
        if name == "Porto Velho":
             query = "Porto Velho, Rondonia, Brazil"
        else:
             # Try appending "Porto Velho, Rondonia"
             query = f"{name}, Porto Velho, Rondonia, Brazil"
        
        lon, lat = get_coordinates(query)
        
        # Retry logic or fallback?
        if lon is None:
             print(f"Not found: {query}. Trying simplified query...")
             query = f"{name}, Rondonia, Brazil"
             lon, lat = get_coordinates(query)
        
        if lon is not None:
            print(f"Found {name}: {lon}, {lat}")
            feat = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat]
                },
                "properties": {
                    "nm_distrito": name,
                    "populacao_2022": info['populacao'],
                    "distancia_sede": info['distancia_sede'],
                    "caracteristicas": info['caracteristicas']
                }
            }
            features.append(feat)
        else:
            print(f"FAILED to find coordinates for {name}")
        
        time.sleep(1.1) # Respect Rate Limit
        
    # Create FeatureCollection
    final_geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    # Save to file
    output_path = os.path.join(os.path.dirname(__file__), '../data_source/distritos_pvh.geojson')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_geojson, f, ensure_ascii=False, indent=2)
    
    print(f"Saved to {output_path}. Total features: {len(features)}")

if __name__ == "__main__":
    main()
