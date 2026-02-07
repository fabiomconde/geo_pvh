import requests
import json
import os

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
     "Rio Pardo": { # Locality
        "populacao": "800",
        "distancia_sede": "320 km",
        "caracteristicas": "Comunidade rural, agricultura familiar, acesso fluvial e terrestre"
    },
}

def normalize(name):
    return name.lower().replace('-', ' ').replace('á', 'a').replace('ã', 'a').replace('ç', 'c').replace('é', 'e').replace('ó', 'o').replace('ô', 'o').strip()

def get_district_names():
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios/1100205/distritos"
    try:
        resp = requests.get(url)
        data = resp.json()
        return {str(d['id']): d['nome'] for d in data}
    except:
        return {}

def main():
    # 1. Fetch District Names (Code -> Name)
    print("Fetching district names...")
    code_map = get_district_names()
    print(f"Found {len(code_map)} district names.")

    # 2. Fetch Geometry (State 11 with District Division - V2 API)
    # Using V2 API resolucao=5 (distrito)
    url_geo = "https://servicodados.ibge.gov.br/api/v2/malhas/11?formato=application/vnd.geo+json&resolucao=5&qualidade=minima"
    print(f"Fetching geometry from {url_geo}...")
    
    try:
        geo_resp = requests.get(url_geo)
        # Check HTTP status
        if geo_resp.status_code != 200:
             print(f"Error fetching: {geo_resp.status_code}")
             return
             
        geo_data = geo_resp.json()
    except Exception as e:
        print(f"Error parse JSON: {e}")
        return

    features = []
    found_count = 0
    
    if 'features' not in geo_data:
        print("Error: No features in state geometry response")
        return

    print(f"Total features in state: {len(geo_data['features'])}")

    for feature in geo_data['features']:
        props = feature['properties']
        cod_area = props.get('codarea') # District Code
        
        # Check if this district belongs to Porto Velho (Starts with 1100205)
        if not str(cod_area).startswith("1100205"):
            continue
            
        # Map Code -> Name (We have the map from Step 1)
        dist_name_ibge = code_map.get(str(cod_area), f"Unknown-{cod_area}")
        props['nm_distrito'] = dist_name_ibge 
        
        # Match Attributes
        data = None
        data = DISTRITOS_DATA.get(dist_name_ibge)
        
        if not data:
             for k, v in DISTRITOS_DATA.items():
                if normalize(k) == normalize(dist_name_ibge):
                    data = v
                    print(f"Matched normalized: {dist_name_ibge} -> {k}")
                    break
        
        if data:
            props['populacao_2022'] = data['populacao']
            props['distancia_sede'] = data['distancia_sede']
            props['caracteristicas'] = data['caracteristicas']
            found_count += 1
        else:
            # print(f"Warning: No attribute data found for {dist_name_ibge} ({cod_area})")
            props['populacao_2022'] = "N/A"
            props['distancia_sede'] = "N/A"
            props['caracteristicas'] = "Sem informações adicionais"
            
        features.append(feature)
            
    print(f"Merged attributes for {found_count} districts.")
    print(f"Total Porto Velho districts found: {len(features)}")

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
    
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
