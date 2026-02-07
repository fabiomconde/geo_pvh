"""
API URL routing
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MunicipioROViewSet, BairroPVHViewSet, DesmatamentoPVHViewSet,
    AlertaDETERViewSet, FocoCalorViewSet, AreaProtegidaViewSet
)

router = DefaultRouter()
router.register(r'municipios', MunicipioROViewSet, basename='municipio')
router.register(r'bairros', BairroPVHViewSet, basename='bairro')
router.register(r'desmatamento', DesmatamentoPVHViewSet, basename='desmatamento')
router.register(r'alertas', AlertaDETERViewSet, basename='alerta')
router.register(r'focos', FocoCalorViewSet, basename='foco')
router.register(r'areas-protegidas', AreaProtegidaViewSet, basename='area-protegida')

urlpatterns = [
    path('', include(router.urls)),
]
