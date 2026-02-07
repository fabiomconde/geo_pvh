import os
from django.contrib.gis.utils import LayerMapping
from core_gis.models import DistritoPVH

# Mapping dictionary: Model Field -> GeoJSON Property
distrito_mapping = {
    'nome': 'name',
    'populacao_2022': 'populacao_2022',
    'distancia_sede': 'distancia_sede',
    'caracteristicas': 'caracteristicas',
    'geom': 'geometry', # GeoJSON geometry
}

geojson_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data_source/distritos_pvh.geojson'))

def run(verbose=True):
    lm = LayerMapping(
        DistritoPVH,
        geojson_file,
        distrito_mapping,
        transform=False, # Data is already in 4326 (from IBGE API)
        encoding='utf-8',
    )
    lm.save(strict=True, verbose=verbose)

if __name__ == "__main__":
    run()
