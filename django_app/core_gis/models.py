"""
GeoDjango models for PVH GeoPortal
"""
from django.contrib.gis.db import models


class MunicipioRO(models.Model):
    """Municípios de Rondônia"""
    gid = models.AutoField(primary_key=True)
    cod_ibge = models.CharField(max_length=10, blank=True, null=True)
    nome = models.CharField(max_length=100)
    uf = models.CharField(max_length=2, default='RO')
    area_km2 = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    populacao = models.IntegerField(null=True)
    geom = models.MultiPolygonField(srid=4326, null=True)

    class Meta:
        managed = False
        db_table = 'geo"."municipios_ro'
        verbose_name = 'Município de RO'
        verbose_name_plural = 'Municípios de RO'

    def __str__(self):
        return self.nome


class BairroPVH(models.Model):
    """Bairros de Porto Velho"""
    gid = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    zona = models.CharField(max_length=50, blank=True, null=True)
    area_km2 = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    populacao = models.IntegerField(null=True)
    geom = models.MultiPolygonField(srid=4326, null=True)

    class Meta:
        managed = False
        db_table = 'geo"."bairros_pvh'
        verbose_name = 'Bairro de Porto Velho'
        verbose_name_plural = 'Bairros de Porto Velho'

    def __str__(self):
        return self.nome


class DesmatamentoPVH(models.Model):
    """Dados de desmatamento PRODES para Porto Velho"""
    gid = models.AutoField(primary_key=True)
    ano = models.IntegerField()
    classe = models.CharField(max_length=50, blank=True, null=True)
    area_ha = models.DecimalField(max_digits=12, decimal_places=4, null=True)
    data_deteccao = models.DateField(null=True)
    fonte = models.CharField(max_length=50, default='PRODES/INPE')
    geom = models.MultiPolygonField(srid=4326, null=True)

    class Meta:
        managed = False
        db_table = 'geo"."desmatamento_pvh'
        verbose_name = 'Desmatamento PVH'
        verbose_name_plural = 'Desmatamentos PVH'
        ordering = ['-ano']

    def __str__(self):
        return f"Desmatamento {self.ano} - {self.area_ha}ha"


class AlertaDETER(models.Model):
    """Alertas DETER de desmatamento"""
    gid = models.AutoField(primary_key=True)
    data_alerta = models.DateField()
    classe = models.CharField(max_length=50)
    area_ha = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    satelite = models.CharField(max_length=50, blank=True, null=True)
    geom = models.MultiPolygonField(srid=4326, null=True)

    class Meta:
        managed = False
        db_table = 'geo"."alertas_deter'
        verbose_name = 'Alerta DETER'
        verbose_name_plural = 'Alertas DETER'
        ordering = ['-data_alerta']

    def __str__(self):
        return f"Alerta {self.data_alerta} - {self.classe}"


class FocoCalor(models.Model):
    """Focos de calor detectados por satélite"""
    gid = models.AutoField(primary_key=True)
    data_hora = models.DateTimeField()
    satelite = models.CharField(max_length=50, blank=True, null=True)
    temperatura_k = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    frp = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    geom = models.PointField(srid=4326, null=True)

    class Meta:
        managed = False
        db_table = 'geo"."focos_calor'
        verbose_name = 'Foco de Calor'
        verbose_name_plural = 'Focos de Calor'
        ordering = ['-data_hora']

    def __str__(self):
        return f"Foco {self.data_hora} - {self.satelite}"


class AreaProtegida(models.Model):
    """Áreas protegidas (UCs, TIs, etc.)"""
    gid = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200)
    categoria = models.CharField(max_length=100, blank=True, null=True)
    esfera = models.CharField(max_length=50, blank=True, null=True)
    area_ha = models.DecimalField(max_digits=14, decimal_places=4, null=True)
    ato_legal = models.CharField(max_length=255, blank=True, null=True)
    ano_criacao = models.IntegerField(null=True)
    geom = models.MultiPolygonField(srid=4326, null=True)

    class Meta:
        managed = False
        db_table = 'geo"."areas_protegidas'
        verbose_name = 'Área Protegida'
        verbose_name_plural = 'Áreas Protegidas'

    def __str__(self):
        return self.nome


class DistritoPVH(models.Model):
    """Distritos de Porto Velho"""
    gid = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    populacao_2022 = models.CharField(max_length=50, blank=True, null=True)
    distancia_sede = models.CharField(max_length=50, blank=True, null=True)
    caracteristicas = models.TextField(blank=True, null=True)
    # Using PointField for compatibility with load script
    geom = models.PointField(srid=4326, null=True)

    class Meta:
        managed = True
        db_table = 'geo"."distritos_pvh'
        verbose_name = 'Distrito de Porto Velho'
        verbose_name_plural = 'Distritos de Porto Velho'

    def __str__(self):
        return self.nome


class LimitePVH(models.Model):
    """Limite Municipal de Porto Velho (Sem distritos)"""
    gid = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, default='Porto Velho')
    geom = models.MultiPolygonField(srid=4326)

    class Meta:
        managed = True
        db_table = 'geo"."limite_pvh'
        verbose_name = 'Limite de Porto Velho'
        verbose_name_plural = 'Limites de Porto Velho'

    def __str__(self):
        return self.nome
