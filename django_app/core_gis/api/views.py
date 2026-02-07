"""
REST Framework API Views with GeoJSON support
"""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_gis.filters import InBBoxFilter
from django.db.models import Sum, Count
from django.core.cache import cache

from ..models import (
    MunicipioRO, BairroPVH, DesmatamentoPVH,
    AlertaDETER, FocoCalor, AreaProtegida
)
from .serializers import (
    MunicipioROSerializer, BairroPVHSerializer, DesmatamentoPVHSerializer,
    AlertaDETERSerializer, FocoCalorSerializer, AreaProtegidaSerializer,DesmatamentoSerializer
)


class MunicipioROViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint para Municípios de Rondônia"""
    queryset = MunicipioRO.objects.all()
    serializer_class = MunicipioROSerializer
    filter_backends = [InBBoxFilter, filters.SearchFilter]
    bbox_filter_field = 'geom'
    search_fields = ['nome', 'cod_ibge']


class BairroPVHViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint para Bairros de Porto Velho"""
    queryset = BairroPVH.objects.all()
    serializer_class = BairroPVHSerializer
    pagination_class = None
    filter_backends = [InBBoxFilter, filters.SearchFilter]
    bbox_filter_field = 'geom'
    search_fields = ['nome', 'zona']
    filterset_fields = ['zona']


class DesmatamentoPVHViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint para dados de Desmatamento PRODES"""
    queryset = DesmatamentoPVH.objects.all()
    serializer_class = DesmatamentoPVHSerializer # Use o serializer padrão do arquivo
    pagination_class = None  # <--- GARANTA QUE ESTA LINHA ESTEJA AQUI
    filter_backends = [InBBoxFilter, filters.SearchFilter, filters.OrderingFilter]
    bbox_filter_field = 'geom'
    search_fields = ['classe']
    filterset_fields = ['ano', 'classe']
    ordering_fields = ['ano', 'area_ha']
    ordering = ['-ano']

    @action(detail=False, methods=['get'])
    def por_ano(self, request):
        """Retorna estatísticas agregadas por ano"""
        cache_key = 'api_desmatamento_por_ano'
        data = cache.get(cache_key)

        if data is None:
            try:
                queryset = self.get_queryset().values('ano').annotate(
                    total_area=Sum('area_ha'),
                    total_poligonos=Count('gid')
                ).order_by('ano')
                data = list(queryset)
                cache.set(cache_key, data, 60 * 60)
            except Exception:
                data = []

        return Response(data)

    @action(detail=False, methods=['get'])
    def por_classe(self, request):
        """Retorna estatísticas agregadas por classe"""
        try:
            queryset = self.get_queryset().values('classe').annotate(
                total_area=Sum('area_ha'),
                total_poligonos=Count('gid')
            ).order_by('-total_area')
            return Response(list(queryset))
        except Exception:
            return Response([])


class AlertaDETERViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint para Alertas DETER"""
    queryset = AlertaDETER.objects.all()
    serializer_class = AlertaDETERSerializer
    filter_backends = [InBBoxFilter, filters.SearchFilter, filters.OrderingFilter]
    bbox_filter_field = 'geom'
    search_fields = ['classe']
    filterset_fields = ['classe', 'satelite']
    ordering_fields = ['data_alerta', 'area_ha']
    ordering = ['-data_alerta']

    @action(detail=False, methods=['get'])
    def por_classe(self, request):
        """Retorna estatísticas agregadas por classe de alerta"""
        try:
            queryset = self.get_queryset().values('classe').annotate(
                total_area=Sum('area_ha'),
                total_alertas=Count('gid')
            ).order_by('-total_alertas')
            return Response(list(queryset))
        except Exception:
            return Response([])


class FocoCalorViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint para Focos de Calor"""
    queryset = FocoCalor.objects.all()
    serializer_class = FocoCalorSerializer
    filter_backends = [InBBoxFilter, filters.OrderingFilter]
    bbox_filter_field = 'geom'
    filterset_fields = ['satelite']
    ordering_fields = ['data_hora', 'temperatura_k']
    ordering = ['-data_hora']


class AreaProtegidaViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint para Áreas Protegidas"""
    queryset = AreaProtegida.objects.all()
    serializer_class = AreaProtegidaSerializer
    filter_backends = [InBBoxFilter, filters.SearchFilter]
    bbox_filter_field = 'geom'
    search_fields = ['nome']
    filterset_fields = ['categoria', 'esfera']
