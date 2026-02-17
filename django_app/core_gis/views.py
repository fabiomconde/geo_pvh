"""
Views for PVH GeoPortal
"""
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.db.models import Sum, Count, Avg
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.conf import settings

from .models import (
    DesmatamentoPVH, AlertaDETER, FocoCalor,
    BairroPVH, MunicipioRO, AreaProtegida, DistritoPVH
)


import os

def home(request):
    """Home page - Dashboard principal"""
    context = {
        'page_title': 'Observatório de Conflitos Socioambientais e Direitos Humanos - Porto Velho',
        'geoserver_url': settings.GEOSERVER_URL,
    }
    return render(request, 'core_gis/home.html', context)


def mapa_desmatamento(request):
    """Mapa interativo de desmatamento (similar ao PRODES)"""
    context = {
        'page_title': 'Mapa de Desmatamento - PRODES',
        'geoserver_url': settings.GEOSERVER_URL,
        'map_center': [-8.76, -63.90],  # Centro de Porto Velho
        'map_zoom': 10,
    }
    return render(request, 'core_gis/mapa/desmatamento.html', context)


def mapa_alertas(request):
    """Mapa de alertas DETER"""
    context = {
        'page_title': 'Mapa de Alertas - DETER',
        'geoserver_url': settings.GEOSERVER_URL,
        'map_center': [-8.76, -63.90],
        'map_zoom': 10,
    }
    return render(request, 'core_gis/mapa/alertas.html', context)


def mapa_focos(request):
    """Mapa de focos de calor"""
    context = {
        'page_title': 'Mapa de Focos de Calor',
        'geoserver_url': settings.GEOSERVER_URL,
        'map_center': [-8.76, -63.90],
        'map_zoom': 10,
    }
    return render(request, 'core_gis/mapa/focos.html', context)


def mapa_distritos(request):
    """Mapa de distritos"""
    context = {
        'page_title': 'Mapa de Distritos',
        'geoserver_url': settings.GEOSERVER_URL,
        'map_center': [-8.76, -63.90],
        'map_zoom': 8,
    }
    return render(request, 'core_gis/mapa/distritos.html', context)


def distritos_geojson(request):
    """API: Retorna os distritos em formato GeoJSON"""
    print("DEBUG: Entered distritos_geojson view")
    from django.core.serializers import serialize
    distritos = DistritoPVH.objects.all()
    print(f"DEBUG: Count {distritos.count()}")
    geojson = serialize('geojson', distritos, geometry_field='geom', fields=('nome', 'populacao_2022', 'distancia_sede', 'caracteristicas'))
    print(f"DEBUG: GeoJSON Type {type(geojson)}")
    return HttpResponse(geojson, content_type='application/json')


def limite_pvh_geojson(request):
    """API: Retorna o limite de Porto Velho em GeoJSON"""
    from core_gis.models import LimitePVH
    from django.core.serializers import serialize
    limite = LimitePVH.objects.all()
    geojson = serialize('geojson', limite, geometry_field='geom', fields=('nome',))
    return HttpResponse(geojson, content_type='application/json')


def dashboard_prodes(request):
    """Dashboard de desmatamento PRODES"""
    context = {
        'page_title': 'Dashboard PRODES - Porto Velho',
    }
    return render(request, 'core_gis/dashboard/prodes.html', context)


def dashboard_deter(request):
    """Dashboard de alertas DETER"""
    context = {
        'page_title': 'Dashboard DETER - Porto Velho',
    }
    return render(request, 'core_gis/dashboard/deter.html', context)


def dashboard_focos(request):
    """Dashboard de focos de calor"""
    context = {
        'page_title': 'Dashboard Focos de Calor - Porto Velho',
    }
    return render(request, 'core_gis/dashboard/focos.html', context)


def sobre(request):
    """Página sobre o projeto"""
    return render(request, 'core_gis/sobre.html', {'page_title': 'Sobre'})


def downloads(request):
    """Página de downloads"""
    return render(request, 'core_gis/downloads.html', {'page_title': 'Downloads'})


def web_services(request):
    """Página de Web Services"""
    context = {
        'page_title': 'Web Services',
        'geoserver_url': settings.GEOSERVER_URL,
    }
    return render(request, 'core_gis/web_services.html', context)


# API Views for Charts and Stats
@cache_page(60 * 15)  # Cache for 15 minutes
def dados_desmatamento_anual(request):
    """API: Dados de desmatamento por ano para gráficos"""
    cache_key = 'desmatamento_anual_stats'
    data = cache.get(cache_key)

    if data is None:
        try:
            queryset = DesmatamentoPVH.objects.values('ano').annotate(
                total_area=Sum('area_ha'),
                total_poligonos=Count('gid')
            ).order_by('ano')

            data = list(queryset)
            cache.set(cache_key, data, 60 * 60)  # Cache 1 hour
        except Exception as e:
            # Return sample data if database not ready
            data = [
                {'ano': 2019, 'total_area': 15234.5, 'total_poligonos': 245},
                {'ano': 2020, 'total_area': 18456.2, 'total_poligonos': 312},
                {'ano': 2021, 'total_area': 12789.8, 'total_poligonos': 198},
                {'ano': 2022, 'total_area': 14567.3, 'total_poligonos': 267},
                {'ano': 2023, 'total_area': 11234.6, 'total_poligonos': 189},
                {'ano': 2024, 'total_area': 9876.4, 'total_poligonos': 156},
            ]

    return JsonResponse(data, safe=False)


@cache_page(60 * 15)
def dados_alertas_mensal(request):
    """API: Dados de alertas DETER por mês"""
    cache_key = 'alertas_mensal_stats'
    data = cache.get(cache_key)

    if data is None:
        try:
            from django.db.models.functions import TruncMonth
            queryset = AlertaDETER.objects.annotate(
                mes=TruncMonth('data_alerta')
            ).values('mes').annotate(
                total_area=Sum('area_ha'),
                total_alertas=Count('gid')
            ).order_by('mes')

            data = [
                {
                    'mes': item['mes'].strftime('%Y-%m') if item['mes'] else None,
                    'total_area': float(item['total_area']) if item['total_area'] else 0,
                    'total_alertas': item['total_alertas']
                }
                for item in queryset
            ]
            cache.set(cache_key, data, 60 * 30)
        except Exception as e:
            data = [
                {'mes': '2024-01', 'total_area': 45.6, 'total_alertas': 12},
                {'mes': '2024-02', 'total_area': 32.1, 'total_alertas': 8},
                {'mes': '2024-03', 'total_area': 18.4, 'total_alertas': 5},
            ]

    return JsonResponse(data, safe=False)


@cache_page(60 * 15)
def dados_focos_diario(request):
    """API: Dados de focos de calor por dia"""
    try:
        from django.db.models.functions import TruncDate
        queryset = FocoCalor.objects.annotate(
            dia=TruncDate('data_hora')
        ).values('dia').annotate(
            total_focos=Count('gid'),
            temp_media=Avg('temperatura_k')
        ).order_by('-dia')[:30]

        data = [
            {
                'dia': item['dia'].strftime('%Y-%m-%d') if item['dia'] else None,
                'total_focos': item['total_focos'],
                'temp_media': float(item['temp_media']) if item['temp_media'] else 0
            }
            for item in queryset
        ]
    except Exception:
        data = [
            {'dia': '2024-08-15', 'total_focos': 2, 'temp_media': 340.35},
            {'dia': '2024-08-16', 'total_focos': 1, 'temp_media': 345.8},
            {'dia': '2024-09-01', 'total_focos': 1, 'temp_media': 340.1},
        ]

    return JsonResponse(data, safe=False)


@cache_page(60 * 60)
def estatisticas_gerais(request):
    """API: Estatísticas gerais do portal"""
    try:
        stats = {
            'total_desmatamento_ha': float(
                DesmatamentoPVH.objects.aggregate(Sum('area_ha'))['area_ha__sum'] or 0
            ),
            'total_alertas': AlertaDETER.objects.count(),
            'total_focos': FocoCalor.objects.count(),
            'total_bairros': BairroPVH.objects.count(),
            'anos_monitoramento': list(
                DesmatamentoPVH.objects.values_list('ano', flat=True).distinct().order_by('ano')
            ),
        }
    except Exception:
        stats = {
            'total_desmatamento_ha': 82158.8,
            'total_alertas': 25,
            'total_focos': 4,
            'total_bairros': 5,
            'anos_monitoramento': [2019, 2020, 2021, 2022, 2023, 2024],
        }

    return JsonResponse(stats)



def icons_preview(request):
    """
    Page to preview all available static icons with pagination.
    """
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

    import os
    from django.conf import settings
    
    # Base directory for images
    images_base_dir = os.path.join(settings.BASE_DIR, 'static', 'images')
    all_icons = []
    
    if os.path.exists(images_base_dir):
        for root, dirs, files in os.walk(images_base_dir):
            for filename in files:
                if filename.lower().endswith('.svg'):
                    # Get relative path from static/images
                    # This handles subdirectories like regular/icon.svg, solid/icon.svg
                    rel_path = os.path.relpath(os.path.join(root, filename), images_base_dir)
                    all_icons.append(rel_path)
    
    # Sort icons for consistent display
    all_icons.sort()
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(all_icons, 300)
    
    try:
        icons = paginator.page(page)
    except PageNotAnInteger:
        icons = paginator.page(1)
    except EmptyPage:
        icons = paginator.page(paginator.num_pages)
    
    context = {
        'page_title': 'Galeria de Ícones',
        'icons': icons,
        'total_icons': len(all_icons),
    }
    return render(request, 'core_gis/icons_preview.html', context)
