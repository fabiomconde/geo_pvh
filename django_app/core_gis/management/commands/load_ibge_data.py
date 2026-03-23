import os
from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import MultiPolygon, Polygon
from core_gis.models import MunicipioRO, LimitePVH, DistritoPVH

class Command(BaseCommand):
    help = 'Carrega dados de municípios e distritos a partir do shapefile RO_distritos_CD2022'

    def handle(self, *args, **options):
        self.stdout.write("Iniciando a carga de dados a partir do shapefile local...")
        
        shp_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'RO_distritos_CD2022',
            'RO_distritos_CD2022.shp'
        )
        
        if not os.path.exists(shp_path):
            self.stdout.write(self.style.ERROR(f"Arquivo não encontrado: {shp_path}"))
            return

        ds = DataSource(shp_path)
        layer = ds[0]
        
        self.stdout.write(f"Shapefile aberto com sucesso. Total de distritos: {len(layer)}")
        
        # Dicionários para agregar as geometrias dos municípios
        municipios_geom = {}
        municipios_nome = {}
        
        distritos_pvh = []
        
        # Helper function
        def ensure_multipolygon(geom):
            if isinstance(geom, Polygon):
                return MultiPolygon(geom)
            elif isinstance(geom, MultiPolygon):
                return geom
            # Em alguns casos raros de union, pode retornar GeometryCollection ou algo diferente
            elif geom.geom_type == 'GeometryCollection':
                polys = [p for p in geom if p.geom_type in ('Polygon', 'MultiPolygon')]
                flattened = []
                for p in polys:
                    if p.geom_type == 'Polygon':
                        flattened.append(p)
                    else:
                        flattened.extend(p)
                return MultiPolygon(*flattened) if flattened else None
            return geom

        # Iterar sobre as feições do shapefile
        for feature in layer:
            cd_mun = str(feature.get('CD_MUN'))
            nm_mun = feature.get('NM_MUN')
            cd_dist = str(feature.get('CD_DIST'))
            nm_dist = feature.get('NM_DIST')
            
            geom = feature.geom.geos
            
            # O SRID do shapefile é 4674 (SIRGAS 2000), vamos transformar para 4326
            if geom.srid != 4326:
                geom.transform(4326)
                
            geom = ensure_multipolygon(geom)
                
            # Agregando geometrias por município
            if cd_mun not in municipios_geom:
                municipios_geom[cd_mun] = geom
                municipios_nome[cd_mun] = nm_mun
            elif geom:
                try:
                    municipios_geom[cd_mun] = municipios_geom[cd_mun].union(geom)
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Erro ao unir geometria do município {nm_mun}: {e}"))
                
            # Coletando distritos de Porto Velho (1100205)
            if cd_mun == '1100205':
                distritos_pvh.append({
                    'cod': cd_dist,
                    'nome': nm_dist,
                    'geom': geom
                })

        self.stdout.write("Atualizando Municípios de RO...")
        for cod_mun, nm_mun in municipios_nome.items():
            geom_mun = municipios_geom[cod_mun]
            geom_mun = ensure_multipolygon(geom_mun)
            
            if not geom_mun:
                continue
            
            mun, created = MunicipioRO.objects.get_or_create(
                cod_ibge=cod_mun,
                defaults={'nome': nm_mun, 'uf': 'RO', 'geom': geom_mun}
            )
            if not created:
                mun.nome = nm_mun
                mun.geom = geom_mun
                mun.save()

        self.stdout.write("Atualizando Distritos de Porto Velho...")
        for dist in distritos_pvh:
            distrito, created = DistritoPVH.objects.get_or_create(
                nome=dist['nome'],
                defaults={'geom': dist['geom']}
            )
            if not created:
                distrito.geom = dist['geom']
                distrito.save()
            self.stdout.write(f"  - Distrito processado: {dist['nome']}")
            
        self.stdout.write("Atualizando Limite de Porto Velho...")
        if '1100205' in municipios_geom:
            geom_pvh = municipios_geom['1100205']
            geom_pvh = ensure_multipolygon(geom_pvh)
                
            if geom_pvh:
                limite, created = LimitePVH.objects.get_or_create(nome="Porto Velho")
                limite.geom = geom_pvh
                limite.save()
                self.stdout.write("Limite de Porto Velho atualizado com sucesso.")
            else:
                self.stdout.write(self.style.WARNING("Falha ao organizar o Limite de Porto Velho em formatação MultiPolygon."))
        else:
            self.stdout.write(self.style.WARNING("Geometria de Porto Velho não encontrada nos dados."))

        self.stdout.write(self.style.SUCCESS('Carga de dados local concluída!'))
