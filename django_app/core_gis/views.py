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
    BairroPVH, MunicipioRO, AreaProtegida, DistritoPVH,
    Publicacao, TipoDocumento, CardSecao, SecaoHome
)


import os


def home(request):
    """Home page - Dashboard principal"""
    
    # Contagem de publicações por tipo de documento
    publicacoes_por_tipo = (
        Publicacao.objects
        .filter(is_publicado=True)
        .values('tipo_documento__nome')
        .annotate(total=Count('id'))
        .order_by('tipo_documento__nome')
    )
    contagem_tipos = {item['tipo_documento__nome']: item['total'] for item in publicacoes_por_tipo}
    total_publicacoes = Publicacao.objects.filter(is_publicado=True).count()

    import json

    # Contagem de publicações por tipo de violação
    violacoes_stats = (
        Publicacao.objects
        .filter(is_publicado=True, violacoes_denunciadas__isnull=False)
        .values('violacoes_denunciadas__nome')
        .annotate(total=Count('id'))
        .order_by('-total')
    )
    chart_labels = [item['violacoes_denunciadas__nome'] for item in violacoes_stats]
    chart_data = [item['total'] for item in violacoes_stats]

    dados_publicacoes = {
        'labels': chart_labels,
        'data': chart_data,
        'datasetLabel': 'Quantidade de Publicações',
        'backgroundColor': 'rgba(249, 115, 22, 0.7)',
        'borderColor': 'rgba(249, 115, 22, 1)',
        'titleText': 'Tipos de Violação',
        'yTitleText': 'Quantidade de Publicações'
    }

    secoes_home = SecaoHome.objects.prefetch_related('cards').order_by('ordem')

    context = {
        'page_title': 'Observatório de Conflitos Socioambientais e Direitos Humanos - Porto Velho',
        'geoserver_url': settings.GEOSERVER_URL,
        'total_publicacoes': total_publicacoes,
        'contagem_tipos': contagem_tipos,
        'secoes_home': secoes_home,
        'dados_publicacoes': json.dumps(dados_publicacoes),
    }

    
    return render(request, 'core_gis/home.html', context)


def mapa_desmatamento(request):
    """Mapa interativo de desmatamento (similar ao PRODES)"""
    context = {
        'tema_class': 'theme-prodes',
        'sidebar_title': 'Camadas',
        'breadcrumbs': [
            {'label': 'Mapas'},
            {'label': 'Desmatamento (PRODES)'}
        ],
        'map_center': [-8.76, -63.90],
        'map_zoom': 10,
        'allow_fullscreen': True,
        'filtros': [
            {
                'titulo': 'Mapa Base',
                'itens': [
                    {'type': 'radio', 'name': 'baseLayer', 'id': 'osmLayer', 'label': 'OpenStreetMap', 'checked': True},
                    {'type': 'radio', 'name': 'baseLayer', 'id': 'satelliteLayer', 'label': 'Satélite', 'checked': False},
                    {'type': 'radio', 'name': 'baseLayer', 'id': 'topoLayer', 'label': 'Topográfico', 'checked': False}
                ]
            },
            {
                'titulo': 'Dados PRODES',
                'itens': [
                    {'type': 'checkbox', 'id': 'desmatamentoLayer', 'label': 'Desmatamento', 'checked': True},
                    {'type': 'checkbox', 'id': 'bairrosLayer', 'label': 'Bairros de PVH', 'checked': False}
                ]
            },
            {
                'titulo': 'Filtrar por Ano',
                'itens': [
                    {'type': 'select', 'id': 'yearFilter', 'options': [
                        {'value': 'all', 'label': 'Todos os anos', 'selected': True},
                        {'value': '2024', 'label': '2024'},
                        {'value': '2023', 'label': '2023'},
                        {'value': '2022', 'label': '2022'},
                        {'value': '2021', 'label': '2021'},
                        {'value': '2020', 'label': '2020'},
                        {'value': '2019', 'label': '2019'}
                    ]}
                ]
            },
            {
                'titulo': 'Legenda',
                'itens': [
                    {'type': 'legend', 'color': 'rgba(220, 53, 69, 0.7)', 'label': 'Desmatamento PRODES'},
                    {'type': 'legend', 'color': 'rgba(13, 110, 253, 0.5)', 'label': 'Limites de Bairros'},
                    {'type': 'info', 'id': 'featureInfo', 'alert_class': 'info', 'icon': 'bi-info-circle', 'title': 'Informações'}
                ]
            }
        ],
        'extra_js_template': 'core_gis/mapa/js_mapa_desmatamento.html'
    }
    return render(request, 'core_gis/mapa/mapa_dinamico.html', context)


def mapa_alertas(request):
    """Mapa de alertas DETER"""
    context = {
        'tema_class': 'theme-deter',
        'sidebar_title': 'Camadas',
        'breadcrumbs': [
            {'label': 'Mapas'},
            {'label': 'Alertas (DETER)'}
        ],
        'map_center': [-8.76, -63.90],
        'map_zoom': 10,
        'allow_fullscreen': True,
        'filtros': [
            {
                'titulo': 'Mapa Base',
                'itens': [
                    {'type': 'radio', 'name': 'baseLayer', 'id': 'osmLayer', 'label': 'OpenStreetMap', 'checked': True},
                    {'type': 'radio', 'name': 'baseLayer', 'id': 'satelliteLayer', 'label': 'Satélite', 'checked': False}
                ]
            },
            {
                'titulo': 'Alertas DETER',
                'itens': [
                    {'type': 'checkbox', 'id': 'alertasLayer', 'label': 'Alertas', 'checked': True}
                ]
            },
            {
                'titulo': 'Legenda',
                'itens': [
                    {'type': 'legend', 'color': 'rgba(255, 193, 7, 0.7)', 'label': 'Desmatamento CR'},
                    {'type': 'legend', 'color': 'rgba(255, 152, 0, 0.7)', 'label': 'Degradação'},
                    {'type': 'legend', 'color': 'rgba(156, 39, 176, 0.7)', 'label': 'Mineração'},
                    {'type': 'info', 'id': 'featureInfo', 'alert_class': 'warning', 'icon': 'bi-exclamation-triangle', 'title': 'Alerta'}
                ]
            }
        ],
        'extra_js_template': 'core_gis/mapa/js_mapa_alertas.html'
    }
    return render(request, 'core_gis/mapa/mapa_dinamico.html', context)


def mapa_focos(request):
    """Mapa de focos de calor"""
    context = {
        'tema_class': 'theme-focos',
        'sidebar_title': 'Camadas',
        'breadcrumbs': [
            {'label': 'Mapas'},
            {'label': 'Focos de Calor'}
        ],
        'map_center': [-8.76, -63.90],
        'map_zoom': 10,
        'allow_fullscreen': True,
        'filtros': [
            {
                'titulo': 'Mapa Base',
                'itens': [
                    {'type': 'radio', 'name': 'baseLayer', 'id': 'osmLayer', 'label': 'OpenStreetMap', 'checked': True},
                    {'type': 'radio', 'name': 'baseLayer', 'id': 'satelliteLayer', 'label': 'Satélite', 'checked': False}
                ]
            },
            {
                'titulo': 'Focos de Calor',
                'itens': [
                    {'type': 'checkbox', 'id': 'focosLayer', 'label': 'Focos Ativos', 'checked': True}
                ]
            },
            {
                'titulo': 'Legenda',
                'itens': [
                    {'type': 'legend', 'color': '#ff5722', 'label': 'Foco de Calor'}
                ]
            }
        ],
        'extra_js_template': 'core_gis/mapa/js_mapa_focos.html'
    }
    return render(request, 'core_gis/mapa/mapa_dinamico.html', context)


def mapa_distritos(request):
    """Mapa de distritos"""
    context = {
        'tema_class': 'theme-default',
        'sidebar_title': 'Camadas',
        'breadcrumbs': [
            {'label': 'Mapas'},
            {'label': 'Distritos'}
        ],
        'map_center': [-9.0, -63.90],
        'map_zoom': 6,
        'allow_fullscreen': True,
        'filtros': [
            {
                'titulo': 'Mapa Base',
                'itens': [
                    {'type': 'radio', 'name': 'baseLayer', 'id': 'osmLayer', 'label': 'OpenStreetMap', 'checked': True}
                ]
            },
            {
                'titulo': 'Limites',
                'itens': [
                    {'type': 'legend', 'color': '#3388ff', 'label': 'Limite Municipal'},
                    {'type': 'info', 'id': 'districtInfo', 'alert_class': 'info', 'icon': 'bi-info-circle', 'title': 'Detalhes do Distrito'}
                ]
            }
        ],
        'extra_js_template': 'core_gis/mapa/js_mapa_distritos.html'
    }
    return render(request, 'core_gis/mapa/mapa_dinamico.html', context)


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
        'tema_class': 'theme-prodes',
        'sidebar_title': 'PRODES',
        'breadcrumbs': [
            {'label': 'Monitoramento'},
            {'label': 'PRODES (Desmatamento)'}
        ],
        'filtros': [
            {
                'titulo': 'Taxas de Desmatamento',
                'itens': [{'label': 'Amazônia Legal', 'icone': 'bi-bar-chart-fill', 'active': True}]
            },
            {
                'titulo': 'Incrementos',
                'itens': [
                    {'label': 'Amazônia Legal', 'icone': 'bi-graph-up-arrow'},
                    {'label': 'Amazônia', 'icone': 'bi-tree'},
                    {'label': 'Não Floresta', 'icone': 'bi-x-circle'}
                ]
            }
        ],
        'header_title': 'Dashboard PRODES',
        'header_subtitle': 'Monitoramento de Desmatamento - Porto Velho, RO',
        'header_icon': 'bi-graph-up',
        'cards': [
            {'icon': 'bi-tree', 'icon_color': 'text-danger', 'valor_inicial': '--', 'label': 'Total Desmatado (ha)', 'id': 'totalArea', 'col_class': 'col-md-3 col-6'},
            {'icon': 'bi-calendar-range', 'icon_color': 'text-primary', 'valor_inicial': '--', 'label': 'Anos Monitorados', 'id': 'totalAnos', 'col_class': 'col-md-3 col-6'},
            {'icon': 'bi-graph-down-arrow', 'icon_color': 'text-success', 'valor_inicial': '--', 'label': 'Último Ano (ha)', 'id': 'ultimoAno', 'col_class': 'col-md-3 col-6'},
            {'icon': 'bi-percent', 'icon_color': 'text-warning', 'valor_inicial': '--', 'label': 'Variação Anual', 'id': 'variacao', 'col_class': 'col-md-3 col-6'}
        ],
        'charts': [
            {'id': 'barChart', 'title': 'Desmatamento Anual em Porto Velho', 'icon': 'bi-bar-chart', 'col_class': 'col-lg-8'},
            {'id': 'pieChart', 'title': 'Distribuição por Período', 'icon': 'bi-pie-chart', 'col_class': 'col-lg-4'},
            {'id': 'lineChart', 'title': 'Evolução Histórica', 'icon': 'bi-graph-up', 'col_class': 'col-12'}
        ],
        'tabela': {
            'title': 'Dados por Ano',
            'icon': 'bi-table',
            'headers': ['Ano', 'Área Desmatada (ha)', 'Polígonos', 'Variação'],
            'body_id': 'dataTable'
        },
        'extra_js_template': 'core_gis/dashboard/js_prodes.html'
    }
    return render(request, 'core_gis/dashboard/dashboard_dinamico.html', context)


def dashboard_deter(request):
    """Dashboard de alertas DETER"""
    context = {
        'tema_class': 'theme-deter',
        'sidebar_title': 'DETER',
        'breadcrumbs': [
            {'label': 'Monitoramento'},
            {'label': 'DETER (Alertas)'}
        ],
        'filtros': [
            {
                'titulo': 'Classes',
                'itens': [
                    {'label': 'Desmatamento CR', 'icone': 'bi-exclamation-triangle-fill', 'active': True},
                    {'label': 'Degradação', 'icone': 'bi-x-octagon'},
                    {'label': 'Mineração', 'icone': 'bi-hammer'},
                ]
            },
            {
                'titulo': 'Período',
                'itens': [
                    {'label': 'Último Mês', 'icone': 'bi-calendar3'},
                    {'label': 'Último Ano', 'icone': 'bi-calendar-range'}
                ]
            }
        ],
        'header_title': 'Dashboard DETER',
        'header_subtitle': 'Alertas de Alteração na Cobertura Florestal - Porto Velho, RO',
        'header_icon': 'bi-exclamation-triangle',
        'cards': [
            {'icon': 'bi-exclamation-triangle', 'icon_color': 'text-warning', 'id': 'totalAlertas', 'label': 'Total de Alertas', 'col_class': 'col-md-4'},
            {'icon': 'bi-geo-alt', 'icon_color': 'text-primary', 'id': 'totalAreaAlertas', 'label': 'Área Total (ha)', 'col_class': 'col-md-4'},
            {'icon': 'bi-calendar', 'icon_color': 'text-success', 'id': 'ultimoAlerta', 'label': 'Último Mês', 'col_class': 'col-md-4'}
        ],
        'charts': [
            {'id': 'barChart', 'title': 'Alertas por Mês', 'icon': 'bi-bar-chart', 'col_class': 'col-lg-8'},
            {'id': 'pieChart', 'title': 'Por Classe', 'icon': 'bi-pie-chart', 'col_class': 'col-lg-4'}
        ],
        'extra_js_template': 'core_gis/dashboard/js_deter.html'
    }
    return render(request, 'core_gis/dashboard/dashboard_dinamico.html', context)


def dashboard_focos(request):
    """Dashboard de focos de calor"""
    context = {
        'tema_class': 'theme-focos',
        'sidebar_title': 'Focos',
        'breadcrumbs': [
            {'label': 'Monitoramento'},
            {'label': 'Focos de Calor'}
        ],
        'filtros': [
            {
                'titulo': 'Satélites',
                'itens': [
                    {'label': 'Todos', 'icone': 'bi-satellite', 'active': True},
                    {'label': 'AQUA', 'icone': 'bi-broadcast'},
                    {'label': 'TERRA', 'icone': 'bi-broadcast'},
                    {'label': 'NPP', 'icone': 'bi-broadcast'}
                ]
            },
            {
                'titulo': 'Período',
                'itens': [
                    {'label': 'Hoje', 'icone': 'bi-calendar-day'},
                    {'label': 'Última Semana', 'icone': 'bi-calendar-week'},
                    {'label': 'Último Mês', 'icone': 'bi-calendar-month'}
                ]
            }
        ],
        'header_title': 'Dashboard Focos de Calor',
        'header_subtitle': 'Monitoramento de Queimadas - Porto Velho, RO',
        'header_icon': 'bi-fire',
        'cards': [
            {'icon': 'bi-fire', 'icon_color': 'text-danger', 'valor_inicial': '--', 'label': 'Total de Focos', 'id': 'totalFocos', 'col_class': 'col-md-3'},
            {'icon': 'bi-thermometer-high', 'icon_color': 'text-warning', 'valor_inicial': '--', 'label': 'Temp. Média (K)', 'id': 'tempMedia', 'col_class': 'col-md-3'},
            {'icon': 'bi-calendar-day', 'icon_color': 'text-primary', 'valor_inicial': '--', 'label': 'Focos Recentes', 'id': 'focosHoje', 'col_class': 'col-md-3'},
            {'icon': 'bi-satellite', 'icon_color': 'text-success', 'valor_inicial': '--', 'label': 'Satélites', 'id': 'satelites', 'col_class': 'col-md-3'}
        ],
        'charts': [
            {'id': 'lineChart', 'title': 'Focos por Dia', 'icon': 'bi-graph-up', 'col_class': 'col-lg-8'},
            {'id': 'pieChart', 'title': 'Por Satélite', 'icon': 'bi-pie-chart', 'col_class': 'col-lg-4'}
        ],
        'extra_js_template': 'core_gis/dashboard/js_focos.html'
    }
    return render(request, 'core_gis/dashboard/dashboard_dinamico.html', context)


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
        # Contagem de publicações por tipo de documento
        publicacoes_por_tipo = (
            Publicacao.objects
            .filter(is_publicado=True)
            .values('tipo_documento__nome')
            .annotate(total=Count('id'))
            .order_by('tipo_documento__nome')
        )
        contagem_tipos = {item['tipo_documento__nome']: item['total'] for item in publicacoes_por_tipo}
        total_publicacoes = Publicacao.objects.filter(is_publicado=True).count()

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
            'total_publicacoes': total_publicacoes,
            'publicacoes_por_tipo': contagem_tipos,
        }
    except Exception:
        stats = {
            'total_desmatamento_ha': 82158.8,
            'total_alertas': 25,
            'total_focos': 4,
            'total_bairros': 5,
            'anos_monitoramento': [2019, 2020, 2021, 2022, 2023, 2024],
            'total_publicacoes': 0,
            'publicacoes_por_tipo': {},
        }

    return JsonResponse(stats)



def lista_publicacoes(request):
    """Página de listagem de publicações com filtros"""
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    from .models import Conflito, TipoViolacao

    publicacoes = Publicacao.objects.filter(is_publicado=True).select_related(
        'tipo_documento', 'conflito'
    ).prefetch_related('violacoes_denunciadas', 'atores_citados')

    # Filtros
    tipo_id = request.GET.get('tipo')
    conflito_id = request.GET.get('conflito')
    violacao_id = request.GET.get('violacao')
    busca = request.GET.get('busca', '').strip()

    if tipo_id:
        publicacoes = publicacoes.filter(tipo_documento_id=tipo_id)
    if conflito_id:
        publicacoes = publicacoes.filter(conflito_id=conflito_id)
    if violacao_id:
        publicacoes = publicacoes.filter(violacoes_denunciadas__id=violacao_id)
    if busca:
        publicacoes = publicacoes.filter(titulo__icontains=busca)

    publicacoes = publicacoes.distinct()

    # Paginação
    paginator = Paginator(publicacoes, 10)
    page = request.GET.get('page', 1)
    try:
        publicacoes_page = paginator.page(page)
    except PageNotAnInteger:
        publicacoes_page = paginator.page(1)
    except EmptyPage:
        publicacoes_page = paginator.page(paginator.num_pages)

    # Dados para filtros na sidebar
    tipos_documento = TipoDocumento.objects.all().order_by('nome')
    conflitos = Conflito.objects.all().order_by('nome')
    violacoes = TipoViolacao.objects.all().order_by('nome')

    context = {
        'page_title': 'Publicações',
        'publicacoes': publicacoes_page,
        'tipos_documento': tipos_documento,
        'conflitos': conflitos,
        'violacoes': violacoes,
        'filtro_tipo': tipo_id,
        'filtro_conflito': conflito_id,
        'filtro_violacao': violacao_id,
        'filtro_busca': busca,
        'total_resultados': paginator.count,
    }
    return render(request, 'core_gis/publicacoes/lista.html', context)


def detalhe_publicacao(request, pk):
    """Página de detalhe de uma publicação"""
    from django.shortcuts import get_object_or_404
    from .models import Publicacao

    publicacao = get_object_or_404(
        Publicacao.objects.select_related('tipo_documento', 'conflito')
        .prefetch_related('violacoes_denunciadas', 'atores_citados'),
        pk=pk,
        is_publicado=True,
    )

    # Publicação anterior e próxima (por data de publicação)
    anterior = (
        Publicacao.objects.filter(is_publicado=True, data_publicacao__lt=publicacao.data_publicacao)
        .order_by('-data_publicacao')
        .first()
    ) if publicacao.data_publicacao else None

    proxima = (
        Publicacao.objects.filter(is_publicado=True, data_publicacao__gt=publicacao.data_publicacao)
        .order_by('data_publicacao')
        .first()
    ) if publicacao.data_publicacao else None

    context = {
        'page_title': publicacao.titulo,
        'publicacao': publicacao,
        'anterior': anterior,
        'proxima': proxima,
    }
    return render(request, 'core_gis/publicacoes/detalhe.html', context)


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


def lista_mapas(request):
    """Página hub listando todos os mapas interativos disponíveis"""
    return render(request, 'core_gis/lista_mapas.html')


def lista_dashboards(request):
    """Página hub listando todos os dashboards disponíveis"""
    return render(request, 'core_gis/lista_dashboards.html')
