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
    path('icons/', views.icons_preview, name='icons_preview'),
    path('publicacoes/', views.lista_publicacoes, name='lista_publicacoes'),
    path('publicacoes/<int:pk>/', views.detalhe_publicacao, name='detalhe_publicacao'),
    path('mapas/', views.lista_mapas, name='lista_mapas'),
    path('dashboards/', views.lista_dashboards, name='lista_dashboards'),

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

    # Rota para abrir o construtor visual e processar o salvamento
    # Rotas de Gestão
    path('dashboards/gestao/', views.listar_dashboards, name='listar_dashboards'),
    path('dashboards/criar/', views.criar_editar_dashboard, name='criar_dashboard'),
    path('dashboards/editar/<int:id>/', views.criar_editar_dashboard, name='editar_dashboard'),
    path('dashboards/excluir/<int:id>/', views.excluir_dashboard, name='excluir_dashboard'),
    
    # Rota para o usuário final visualizar o dashboard gerado
    path('dashboard/<slug:slug>/', views.visualizar_dashboard, name='visualizar_dashboard'),    
]
