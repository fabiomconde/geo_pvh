import os
import sys
import django
import requests
import json
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Polygon

# Setup Django Environment
sys.path.append('/app')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from core_gis.models import LimitePVH

# IBGE V2 API for Porto Velho (1100205)
URL = "https://servicodados.ibge.gov.br/api/v2/malhas/1100205?formato=application/vnd.geo+json&resolucao=5&qualidade=minima"

def run():
    print("Fetching Porto Velho Boundary from IBGE...")
    try:
        resp = requests.get(URL)
        data = resp.json()
        
        if data.get('type') == 'Feature' or data.get('type') == 'FeatureCollection':
            # Handle both single Feature or FeatureCollection
            features = data.get('features') if data.get('type') == 'FeatureCollection' else [data]
            
            # Clear existing
            print(f"Clearing {LimitePVH.objects.count()} existing records...")
            LimitePVH.objects.all().delete()
            
            for feat in features:
                geom_json = json.dumps(feat.get('geometry'))
                geom = GEOSGeometry(geom_json)
                
                # Force MultiPolygon
                if isinstance(geom, Polygon):
                    geom = MultiPolygon(geom)
                
                limit = LimitePVH.objects.create(
                    nome='Porto Velho (Limite Municipal)',
                    geom=geom
                )
                print(f"Limite Municipal saved! ID: {limit.gid}")
        else:
            print("Invalid GeoJSON Format")
            print(data.keys())
            
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run()
