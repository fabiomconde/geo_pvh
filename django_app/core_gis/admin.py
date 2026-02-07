from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from .models import (
    MunicipioRO, BairroPVH, DesmatamentoPVH,
    AlertaDETER, FocoCalor, AreaProtegida, DistritoPVH
)


@admin.register(MunicipioRO)
class MunicipioROAdmin(GISModelAdmin):
    list_display = ('nome', 'cod_ibge', 'area_km2', 'populacao')
    search_fields = ('nome', 'cod_ibge')
    readonly_fields = ('gid',)


@admin.register(BairroPVH)
class BairroPVHAdmin(GISModelAdmin):
    list_display = ('nome', 'zona', 'area_km2', 'populacao')
    search_fields = ('nome', 'zona')
    list_filter = ('zona',)


@admin.register(DesmatamentoPVH)
class DesmatamentoPVHAdmin(GISModelAdmin):
    list_display = ('ano', 'classe', 'area_ha', 'data_deteccao', 'fonte')
    list_filter = ('ano', 'classe', 'fonte')
    search_fields = ('classe',)


@admin.register(AlertaDETER)
class AlertaDETERAdmin(GISModelAdmin):
    list_display = ('data_alerta', 'classe', 'area_ha', 'satelite')
    list_filter = ('classe', 'satelite')
    date_hierarchy = 'data_alerta'


@admin.register(FocoCalor)
class FocoCalorAdmin(GISModelAdmin):
    list_display = ('data_hora', 'satelite', 'temperatura_k', 'frp')
    list_filter = ('satelite',)
    date_hierarchy = 'data_hora'


@admin.register(AreaProtegida)
class AreaProtegidaAdmin(GISModelAdmin):
    list_display = ('nome', 'categoria', 'esfera', 'area_ha', 'ano_criacao')
    list_filter = ('categoria', 'esfera')
    search_fields = ('nome',)

@admin.register(DistritoPVH)
class DistritoPVHAdmin(GISModelAdmin):
    list_display = ('nome', 'populacao_2022', 'distancia_sede')
    search_fields = ('nome',)
