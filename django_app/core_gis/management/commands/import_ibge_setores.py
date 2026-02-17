import os
from django.core.management.base import BaseCommand
from django.contrib.gis.utils import LayerMapping
from core_gis.models import SetorCensitario

class Command(BaseCommand):
    help = 'Importa setores censitários do IBGE para o PostGIS'

    def handle(self, *args, **options):
        # Caminho do arquivo dentro do container
        geojson_file = '/app/data_source/geojson_import/setores_pvh.json.geojson'
        
        # Mapeamento: 'Nome no Model': 'NOME_NO_GEOJSON'
        # Verifique os nomes das colunas no seu GeoJSON (geralmente em maiúsculas)
        mapping = {
            'cd_setor': 'CD_SETOR',
            'situacao': 'SITUACAO',
            'nm_regiao': 'NM_REGIAO',
            'area_km2': 'AREA_KM2',
            'geom': 'MULTIPOLYGON', # Ou 'POLYGON' dependendo do arquivo
        }

        try:
            lm = LayerMapping(
                SetorCensitario, geojson_file, mapping,
                transform=False, encoding='utf-8'
            )
            lm.save(strict=True, verbose=True)
            self.stdout.write(self.style.SUCCESS('Dados importados com sucesso!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro na importação: {e}'))