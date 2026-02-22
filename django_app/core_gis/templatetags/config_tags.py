from django import template
from django.utils.safestring import mark_safe
from core_gis.models import Configuracao

register = template.Library()

@register.simple_tag
def get_configuracao(identificador):
    """
    Retorna o corpo de texto de uma Configuracao baseada no seu identificador.
    Se não encontrar, retorna uma string vazia.
    """
    try:
        config = Configuracao.objects.get(identificador=identificador)
        return mark_safe(config.corpo_texto)
    except Configuracao.DoesNotExist:
        return ""
