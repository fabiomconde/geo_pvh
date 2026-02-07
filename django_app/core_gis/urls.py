"""
URL patterns for core_gis app
"""
from django.urls import path
from . import views

app_name = 'core_gis'

urlpatterns = [
    # Pages
    path('', views.home, name='home'),
    path('sobre/', views.sobre, name='sobre'),
    path('downloads/', views.downloads, name='downloads'),
    path('web-services/', views.web_services, name='web_services'),

    # Maps
    path('mapa/desmatamento/', views.mapa_desmatamento, name='mapa_desmatamento'),
    path('mapa/alertas/', views.mapa_alertas, name='mapa_alertas'),
    path('mapa/focos/', views.mapa_focos, name='mapa_focos'),
    path('mapa/distritos/', views.mapa_distritos, name='mapa_distritos'),

    # Dashboards
    path('dashboard/prodes/', views.dashboard_prodes, name='dashboard_prodes'),
    path('dashboard/deter/', views.dashboard_deter, name='dashboard_deter'),
    path('dashboard/focos/', views.dashboard_focos, name='dashboard_focos'),

    # Chart data endpoints
    path('dados/desmatamento-anual/', views.dados_desmatamento_anual, name='dados_desmatamento_anual'),
    path('dados/alertas-mensal/', views.dados_alertas_mensal, name='dados_alertas_mensal'),
    path('dados/focos-diario/', views.dados_focos_diario, name='dados_focos_diario'),
    path('dados/focos-diario/', views.dados_focos_diario, name='dados_focos_diario'),
    path('dados/estatisticas/', views.estatisticas_gerais, name='estatisticas_gerais'),
    path('api/distritos-geojson/', views.distritos_geojson, name='distritos_geojson'),
    path('api/limite-pvh-geojson/', views.limite_pvh_geojson, name='limite_pvh_geojson'),
]
