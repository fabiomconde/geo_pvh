from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from .models import (
    MunicipioRO, BairroPVH, DesmatamentoPVH,
    AlertaDETER, FocoCalor, AreaProtegida, DistritoPVH,
    TipoDocumento, FaseConflito, TipoTerritorio, Bioma, TipoAtor, PapelAtor, SetorEconomico, DireitoAfetado, TipoViolacao,
    Localizacao, Ator, Conflito, EnvolvimentoAtor, Publicacao, PublicacaoImagem, Configuracao,
    SecaoHome, CardSecao
)

@admin.register(Configuracao)
class ConfiguracaoAdmin(admin.ModelAdmin):
    list_display = ('identificador', 'data_alteracao', 'usuario')
    search_fields = ('identificador',)
    readonly_fields = ('data_criacao', 'data_alteracao')

    def save_model(self, request, obj, form, change):
        if not obj.usuario:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)


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


@admin.register(TipoDocumento)
class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(FaseConflito)
class FaseConflitoAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(TipoTerritorio)
class TipoTerritorioAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(Bioma)
class BiomaAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(TipoAtor)
class TipoAtorAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(PapelAtor)
class PapelAtorAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(SetorEconomico)
class SetorEconomicoAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(DireitoAfetado)
class DireitoAfetadoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')

@admin.register(TipoViolacao)
class TipoViolacaoAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(Localizacao)
class LocalizacaoAdmin(admin.ModelAdmin):
    list_display = ('nome_territorio', 'tipo', 'municipio', 'estado')
    list_filter = ('tipo', 'bioma')
    search_fields = ('nome_territorio', 'municipio')

@admin.register(Ator)
class AtorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'setor_economico', 'dados_sensiveis')
    list_filter = ('tipo', 'setor_economico')
    search_fields = ('nome', 'cnpj_cpf')

class EnvolvimentoAtorInline(admin.TabularInline):
    model = EnvolvimentoAtor
    extra = 1

@admin.register(Conflito)
class ConflitoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'fase_atual', 'data_inicio', 'data_fim')
    list_filter = ('fase_atual', 'data_inicio')
    search_fields = ('nome', 'resumo')
    inlines = [EnvolvimentoAtorInline]
    filter_horizontal = ('localizacoes', 'direitos_afetados')

class PublicacaoImagemInline(admin.TabularInline):
    model = PublicacaoImagem
    extra = 1

@admin.register(Publicacao)
class PublicacaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo_documento', 'data_fato', 'is_publicado', 'is_restrito')
    list_filter = ('tipo_documento', 'is_publicado', 'is_restrito', 'data_fato')
    search_fields = ('titulo', 'fonte_original')
    filter_horizontal = ('atores_citados', 'violacoes_denunciadas')
    inlines = [PublicacaoImagemInline]
    # O RichTextField será renderizado automaticamente no form padrão


class CardSecaoInline(admin.StackedInline):
    model = CardSecao
    extra = 1

@admin.register(SecaoHome)
class SecaoHomeAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'ordem', 'cor_fundo')
    list_editable = ('tipo', 'ordem', 'cor_fundo')
    search_fields = ('titulo', 'subtitulo')
    inlines = [CardSecaoInline]
