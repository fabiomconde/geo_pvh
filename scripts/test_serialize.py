from django.core.serializers import serialize
from core_gis.models import DistritoPVH
import json

try:
    distritos = DistritoPVH.objects.all()
    print(f"Count: {distritos.count()}")
    
    # Test 1: Full fields
    print("Testing serialize full...")
    data = serialize('geojson', distritos, geometry_field='geom', fields=('nome', 'populacao_2022', 'distancia_sede', 'caracteristicas'))
    print("Serialize success!")
    # print(data[:100])
except Exception as e:
    import traceback
    traceback.print_exc()
