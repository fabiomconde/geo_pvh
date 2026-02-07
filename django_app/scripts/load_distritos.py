import os
from django.contrib.gis.utils import LayerMapping
from core_gis.models import DistritoPVH

# Mapping dictionary: Model Field -> GeoJSON Property
# FROM HEAD OUTPUT: "properties": { "id": "110020505", "name": "Abunã", ... }
# Wait, the output below shows "name".
# Let's check the previous error: "ValueError: 'name' is not in list" from OGR.
# This usually means the OGR driver (GeoJSON) isn't seeing the field 'name'.
# Sometimes GeoJSON fields are case sensitive or truncated.
# I'll enable verbose=True in the script to see available fields.

distrito_mapping = {
    'nome': 'nm_distrito', # Correct key from IBGE
    'populacao_2022': 'populacao_2022',
    'distancia_sede': 'distancia_sede',
    'caracteristicas': 'caracteristicas',
    'geom': 'POINT', # Use geometry type for layer mapping
}

geojson_file = '/app/data_source/distritos_pvh.geojson'

def run(verbose=True):
    print(f"Loading data from {geojson_file}")
    
    # Debug: Check layers
    from django.contrib.gis.gdal import DataSource
    ds = DataSource(geojson_file)
    layer = ds[0]
    print("Available fields in GeoJSON:", layer.fields)
    
    lm = LayerMapping(
        DistritoPVH,
        geojson_file,
        distrito_mapping,
        transform=False, 
        encoding='utf-8',
    )
    lm.save(strict=True, verbose=verbose)
    print("Data loaded successfully.")

if __name__ == "__main__":
    run()
