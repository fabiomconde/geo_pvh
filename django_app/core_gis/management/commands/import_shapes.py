"""
Management command to import Shapefiles into PostGIS
"""
import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon
from django.db import connection

from core_gis.models import DesmatamentoPVH, BairroPVH


class Command(BaseCommand):
    help = 'Import shapefiles into PostGIS database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--shapefile',
            type=str,
            help='Path to the shapefile to import'
        )
        parser.add_argument(
            '--type',
            type=str,
            choices=['desmatamento', 'bairros', 'municipios'],
            help='Type of data to import'
        )
        parser.add_argument(
            '--filter-municipio',
            type=str,
            default='PORTO VELHO',
            help='Filter by municipality name (default: PORTO VELHO)'
        )
        parser.add_argument(
            '--srid',
            type=int,
            default=4326,
            help='Source SRID (default: 4326)'
        )

    def handle(self, *args, **options):
        shapefile = options['shapefile']
        data_type = options['type']
        filter_municipio = options['filter_municipio']
        srid = options['srid']

        if not shapefile:
            self.stdout.write(self.style.WARNING(
                'No shapefile provided. Running with sample data...'
            ))
            self._insert_sample_data()
            return

        if not os.path.exists(shapefile):
            raise CommandError(f'Shapefile not found: {shapefile}')

        self.stdout.write(f'Importing {shapefile}...')

        try:
            ds = DataSource(shapefile)
            layer = ds[0]

            self.stdout.write(f'Layer: {layer.name}')
            self.stdout.write(f'Features: {len(layer)}')
            self.stdout.write(f'Fields: {layer.fields}')

            if data_type == 'desmatamento':
                self._import_desmatamento(layer, filter_municipio, srid)
            elif data_type == 'bairros':
                self._import_bairros(layer, srid)
            else:
                self.stdout.write(self.style.WARNING(
                    f'Import type {data_type} not implemented yet'
                ))

        except Exception as e:
            raise CommandError(f'Error importing shapefile: {e}')

    def _import_desmatamento(self, layer, filter_municipio, srid):
        """Import PRODES deforestation data"""
        count = 0
        for feature in layer:
            # Try to filter by municipality
            municipio = None
            for field in ['municipio', 'nm_mun', 'MUNICIPIO', 'NM_MUN']:
                try:
                    municipio = feature.get(field)
                    break
                except:
                    continue

            if municipio and filter_municipio.upper() not in str(municipio).upper():
                continue

            # Get geometry
            geom = feature.geom
            if geom.geom_type == 'Polygon':
                geom = MultiPolygon(geom.geos)
            else:
                geom = geom.geos

            # Get year
            ano = None
            for field in ['ano', 'ANO', 'year', 'YEAR']:
                try:
                    ano = int(feature.get(field))
                    break
                except:
                    continue

            # Get area
            area_ha = None
            for field in ['area_ha', 'AREA_HA', 'areaha', 'AREAHA']:
                try:
                    area_ha = float(feature.get(field))
                    break
                except:
                    continue

            if ano:
                DesmatamentoPVH.objects.create(
                    ano=ano,
                    classe='DESMATAMENTO',
                    area_ha=area_ha or geom.area * 111319.9 ** 2 / 10000,  # Rough conversion
                    geom=geom
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Successfully imported {count} deforestation polygons'
        ))

    def _import_bairros(self, layer, srid):
        """Import neighborhood data"""
        count = 0
        for feature in layer:
            geom = feature.geom
            if geom.geom_type == 'Polygon':
                geom = MultiPolygon(geom.geos)
            else:
                geom = geom.geos

            nome = None
            for field in ['nome', 'NOME', 'name', 'NAME', 'nm_bairro']:
                try:
                    nome = feature.get(field)
                    break
                except:
                    continue

            if nome:
                BairroPVH.objects.create(
                    nome=nome,
                    geom=geom
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Successfully imported {count} neighborhoods'
        ))

    def _insert_sample_data(self):
        """Insert sample data if no shapefile provided"""
        self.stdout.write('Inserting sample data...')

        # Sample data is already in init_db.sql
        self.stdout.write(self.style.SUCCESS(
            'Sample data available in database via init_db.sql'
        ))
