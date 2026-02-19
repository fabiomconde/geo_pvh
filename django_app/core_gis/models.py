from django.contrib.gis.db import models
from django_ckeditor_5.fields import CKEditor5Field 



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


class SetorCensitario(models.Model):
    # Campos baseados na tabela do IBGE que vimos no seu print
    cd_setor = models.CharField(max_length=15, unique=True)
    situacao = models.CharField(max_length=50, null=True, blank=True)
    nm_regiao = models.CharField(max_length=50, null=True, blank=True)
    area_km2 = models.FloatField(null=True)
    
    # O campo geométrico (MultiPolygon para garantir compatibilidade)
    geom = models.MultiPolygonField(srid=4674)

    class Meta:
        managed = True
        db_table = '"geo"."core_gis_setorcensitario"' # Força o esquema geo

    def __str__(self):
        return self.cd_setor



# =============================================================================
# 1. MODELOS DE TAXONOMIA
# =============================================================================

class TipoDocumento(models.Model):
    nome = models.CharField("Tipo de Documento", max_length=100, unique=True)
    def __str__(self): return self.nome

class FaseConflito(models.Model):
    nome = models.CharField("Fase do Conflito", max_length=100, unique=True)
    def __str__(self): return self.nome

class TipoTerritorio(models.Model):
    nome = models.CharField("Tipo de Território", max_length=100, unique=True)
    def __str__(self): return self.nome

class Bioma(models.Model):
    nome = models.CharField("Bioma", max_length=100, unique=True)
    def __str__(self): return self.nome

class TipoAtor(models.Model):
    nome = models.CharField("Tipo de Ator", max_length=100, unique=True)
    def __str__(self): return self.nome

class PapelAtor(models.Model):
    nome = models.CharField("Papel do Ator", max_length=100, unique=True)
    def __str__(self): return self.nome

class SetorEconomico(models.Model):
    nome = models.CharField("Setor Econômico", max_length=100, unique=True)
    def __str__(self): return self.nome

class DireitoAfetado(models.Model):
    nome = models.CharField("Direito Afetado", max_length=150, unique=True)
    descricao = models.TextField("Descrição", blank=True, null=True)
    def __str__(self): return self.nome

class TipoViolacao(models.Model):
    nome = models.CharField("Tipo de Violação", max_length=150, unique=True)
    def __str__(self): return self.nome

# =============================================================================
# 2. MODELOS PRINCIPAIS
# =============================================================================

class Localizacao(models.Model):
    nome_territorio = models.CharField("Nome do Território", max_length=200)
    tipo = models.ForeignKey(TipoTerritorio, on_delete=models.SET_NULL, null=True)
    bioma = models.ForeignKey(Bioma, on_delete=models.SET_NULL, null=True)
    municipio = models.CharField("Município", max_length=150)
    estado = models.CharField("Estado", max_length=2)
    # Latitude/Longitude usando Decimal para precisão
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    def __str__(self):
        return f"{self.nome_territorio} ({self.municipio}-{self.estado})"

class Ator(models.Model):
    nome = models.CharField("Nome", max_length=255)
    tipo = models.ForeignKey(TipoAtor, on_delete=models.SET_NULL, null=True)
    setor_economico = models.ForeignKey(SetorEconomico, on_delete=models.SET_NULL, null=True, blank=True)
    cnpj_cpf = models.CharField("CNPJ/Registro", max_length=50, blank=True, null=True)
    
    # Campo CKEditor 5
    historico = CKEditor5Field("Histórico do Ator", config_name='extends', blank=True, null=True)
    
    dados_sensiveis = models.BooleanField("Dados Sensíveis", default=False)

    class Meta:
        verbose_name_plural = "Atores"

    def __str__(self): return self.nome

# =============================================================================
# 3. CONFLITO
# =============================================================================

class Conflito(models.Model):
    nome = models.CharField("Nome do Caso", max_length=255)
    resumo = models.TextField("Resumo Curto")
    
    # Campo CKEditor 5 para narrativa longa com fotos/vídeos
    historico_completo = CKEditor5Field("Histórico Detalhado", config_name='extends')
    
    fase_atual = models.ForeignKey(FaseConflito, on_delete=models.SET_NULL, null=True)
    localizacoes = models.ManyToManyField(Localizacao, related_name="conflitos")
    direitos_afetados = models.ManyToManyField(DireitoAfetado, blank=True)
    
    data_inicio = models.DateField("Data Início", blank=True, null=True)
    data_fim = models.DateField("Data Fim", blank=True, null=True)
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self): return self.nome

class EnvolvimentoAtor(models.Model):
    conflito = models.ForeignKey(Conflito, on_delete=models.CASCADE)
    ator = models.ForeignKey(Ator, on_delete=models.CASCADE)
    papel = models.ForeignKey(PapelAtor, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('conflito', 'ator', 'papel')
        verbose_name = "Envolvimento de Ator"
        verbose_name_plural = "Envolvimentos de Atores"

    def __str__(self):
        return f"{self.ator} como {self.papel} em {self.conflito}"

# =============================================================================
# 4. PUBLICAÇÃO
# =============================================================================

class Publicacao(models.Model):
    titulo = models.CharField("Título", max_length=255)
    subtitulo = models.CharField("Subtítulo", max_length=255, blank=True, null=True)
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.SET_NULL, null=True)
    
    # Campo CKEditor 5 Principal
    corpo_texto = CKEditor5Field("Conteúdo", config_name='extends')
    
    conflito = models.ForeignKey(Conflito, on_delete=models.SET_NULL, null=True, blank=True, related_name="publicacoes")
    atores_citados = models.ManyToManyField(Ator, blank=True)
    violacoes_denunciadas = models.ManyToManyField(TipoViolacao, blank=True)
    
    data_fato = models.DateField("Data do Fato", blank=True, null=True)
    data_publicacao = models.DateTimeField("Data da Publicação", blank=True, null=True)
    fonte_original = models.CharField("Fonte", max_length=150, blank=True, null=True)
    
    anexo_pdf = models.FileField("Anexo (PDF)", upload_to='publicacoes/anexos/', blank=True, null=True)
    
    is_publicado = models.BooleanField("Publicado?", default=False)
    is_restrito = models.BooleanField("Restrito?", default=False)
    
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Publicação"
        verbose_name_plural = "Publicações"
        ordering = ['-data_publicacao']

    def __str__(self):
        return self.titulo
