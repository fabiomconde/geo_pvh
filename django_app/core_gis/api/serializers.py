"""
REST Framework GIS Serializers
"""
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from ..models import (
    MunicipioRO, BairroPVH, DesmatamentoPVH,
    AlertaDETER, FocoCalor, AreaProtegida
)


class MunicipioROSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = MunicipioRO
        geo_field = 'geom'
        fields = ('gid', 'cod_ibge', 'nome', 'uf', 'area_km2', 'populacao')


class BairroPVHSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = BairroPVH
        geo_field = 'geom'
        fields = ('gid', 'nome', 'zona', 'area_km2', 'populacao')


class DesmatamentoPVHSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = DesmatamentoPVH
        geo_field = 'geom' # Certifique-se que no models.py o campo se chama 'geom'
        fields = ('gid', 'ano', 'classe', 'area_ha', 'data_deteccao', 'fonte')


class DesmatamentoPVHStatsSerializer(serializers.Serializer):
    """Serializer for aggregated stats"""
    ano = serializers.IntegerField()
    total_area = serializers.DecimalField(max_digits=14, decimal_places=4)
    total_poligonos = serializers.IntegerField()


class AlertaDETERSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = AlertaDETER
        geo_field = 'geom'
        fields = ('gid', 'data_alerta', 'classe', 'area_ha', 'satelite')


class FocoCalorSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = FocoCalor
        geo_field = 'geom'
        fields = ('gid', 'data_hora', 'satelite', 'temperatura_k', 'frp')


class AreaProtegidaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = AreaProtegida
        geo_field = 'geom'
        fields = ('gid', 'nome', 'categoria', 'esfera', 'area_ha', 'ato_legal', 'ano_criacao')

class DesmatamentoSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = DesmatamentoPVH
        geo_field = "geom"
        fields = "__all__"