from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field 

class Configuracao(models.Model):
    """Configurações dinâmicas de textos e informações do sistema"""
    identificador = models.CharField("Identificador", max_length=100, unique=True, help_text="Ex: sobre, mensagem_inicio, rodape_informativo")
    corpo_texto = CKEditor5Field("Conteúdo", config_name='extends')
    data_criacao = models.DateTimeField("Data de Criação", auto_now_add=True)
    data_alteracao = models.DateTimeField("Data de Alteração", auto_now=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Usuário")

    class Meta:
        verbose_name = "Configuração do Sistema"
        verbose_name_plural = "Configurações do Sistema"

    def __str__(self):
        return self.identificador 

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
    geom = models.MultiPolygonField(srid=4326, null=True)

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


class PublicacaoImagem(models.Model):
    publicacao = models.ForeignKey(Publicacao, related_name='imagens', on_delete=models.CASCADE)
    imagem = models.ImageField("Imagem", upload_to='publicacoes/imagens/')
    ordem = models.PositiveIntegerField("Ordem", default=0, help_text="Define a ordem de exibição. A primeira (menor número) será a capa da publicação.")
    legenda = models.CharField("Legenda", max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Imagem da Publicação"
        verbose_name_plural = "Imagens da Publicação"
        ordering = ['ordem']

    def __str__(self):
        return f"Imagem {self.ordem} - {self.publicacao.titulo}"


# =============================================================================
# 5. CONTEÚDOS DINÂMICOS (HOME)
# =============================================================================

class SecaoHome(models.Model):
    TIPO_CHOICES = [
        ('publicacao', 'Publicação'),
        ('dashboard', 'Dashboard'),
        ('mapa', 'Mapa Interativo'),
    ]
    
    titulo = models.CharField("Título", max_length=200)
    subtitulo = models.CharField("Subtítulo", max_length=255, blank=True, null=True)
    tipo = models.CharField("Tipo da Seção", max_length=20, choices=TIPO_CHOICES, default='publicacao')
    icone = models.CharField("Ícone (SVG)", max_length=100, help_text="Nome do arquivo SVG do ícone (ex: 'chart-line.svg')")
    cor_fundo = models.CharField("Variável de Cor do Fundo", max_length=100, default='var(--theme-bg-white)', help_text="Cor ou variável CSS de fundo da seção")
    ordem = models.PositiveIntegerField("Ordem de Exibição", default=0)
    url = models.CharField("URL", default='#', max_length=255, help_text="URL ou nome da rota (ex: 'core_gis:lista_mapas')")

    class Meta:
        verbose_name = "Seção da Home"
        verbose_name_plural = "Seções da Home"
        ordering = ['ordem']

    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_display()})"

class CardSecao(models.Model):
    secao = models.ForeignKey(SecaoHome, related_name='cards', on_delete=models.CASCADE, verbose_name="Seção")
    titulo = models.CharField("Título do Card", max_length=200)
    subtitulo = models.TextField("Subtítulo/Descrição", blank=True, null=True)
    url = models.CharField("URL", max_length=255, help_text="URL ou nome da rota (ex: 'core_gis:lista_mapas')")
    icone = models.CharField("Ícone (SVG)", max_length=100, help_text="Nome do arquivo SVG do ícone da badge")
    texto_botao = models.CharField("Texto do Botão", max_length=100, default="Acessar")
    btn_class = models.CharField("Classe CSS do Botão", max_length=50, default="btn-primary", help_text="ex: btn-primary")
    badge_text = models.CharField("Texto da Badge", max_length=50, blank=True, null=True)
    badge_class = models.CharField("Classe CSS da Badge", max_length=50, blank=True, null=True, help_text="ex: theme-forest")
    ordem = models.PositiveIntegerField("Ordem de Exibição", default=0)

    class Meta:
        verbose_name = "Card da Seção"
        verbose_name_plural = "Cards da Seção"
        ordering = ['ordem']

    def __str__(self):
        return f"{self.titulo} - {self.secao.titulo}"


from django.db import models
from django.core.validators import FileExtensionValidator
import csv
import io

# =============================================================================
# DASHBOARD DINÂMICO
# =============================================================================

class DashboardDinamico(models.Model):
    titulo = models.CharField("Título do Dashboard", max_length=200)
    subtitulo = models.CharField("Subtítulo", max_length=255, blank=True, null=True)
    slug = models.SlugField("URL Slug", unique=True)
    tema_class = models.CharField("Tema CSS", max_length=50, default="theme-default", help_text="Ex: theme-deter, theme-prodes")
    icone_header = models.CharField("Ícone do Cabeçalho", max_length=50, default="bi-graph-up")
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo

class Linha(models.Model):
    dashboard = models.ForeignKey(DashboardDinamico, related_name='linhas', on_delete=models.CASCADE)
    ordem = models.PositiveIntegerField("Ordem", default=0)

    class Meta:
        ordering = ['ordem']

    def __str__(self):
        return f"Linha {self.ordem} - {self.dashboard.titulo}"

class Coluna(models.Model):
    TIPO_CONTEUDO =[
        ('quadros', 'Lista de Quadros (Stat Cards)'),
        ('tabela', 'Tabela de Dados'),
        ('grafico', 'Gráfico'),
    ]
    TAMANHO_CHOICES =[
        ('col-12', 'Largura Total (100%)'),
        ('col-lg-8', 'Larga (66%)'),
        ('col-lg-6', 'Metade (50%)'),
        ('col-lg-4', 'Estreita (33%)'),
        ('col-lg-3', 'Muito Estreita (25%)'),
    ]

    linha = models.ForeignKey(Linha, related_name='colunas', on_delete=models.CASCADE)
    tamanho_css = models.CharField("Tamanho da Coluna", max_length=20, choices=TAMANHO_CHOICES, default='col-lg-6')
    tipo_conteudo = models.CharField("Tipo de Conteúdo", max_length=20, choices=TIPO_CONTEUDO)
    ordem = models.PositiveIntegerField("Ordem na Linha", default=0)

    class Meta:
        ordering = ['ordem']

    def __str__(self):
        return f"Coluna ({self.get_tamanho_css_display()}) - {self.get_tipo_conteudo_display()}"

# --- Componentes Internos das Colunas ---

class Quadro(models.Model):
    """Corresponde aos 'Stat Cards' com números"""
    coluna = models.ForeignKey(Coluna, related_name='quadros', on_delete=models.CASCADE)
    titulo = models.CharField("Título/Label", max_length=100)
    valor = models.CharField("Valor (Número ou Texto)", max_length=50)
    icone = models.CharField("Ícone (Bootstrap Icons)", max_length=50, default="bi-bar-chart")
    icone_cor = models.CharField("Cor do Ícone (Classe CSS)", max_length=50, default="text-primary", help_text="Ex: text-danger, text-success")
    ordem = models.PositiveIntegerField("Ordem", default=0)

    class Meta:
        ordering = ['ordem']

class TabelaDinamica(models.Model):
    """Aceita upload de CSV e converte para JSON Editável"""
    coluna = models.OneToOneField(Coluna, related_name='tabela', on_delete=models.CASCADE)
    titulo = models.CharField("Título da Tabela", max_length=200)
    icone = models.CharField("Ícone", max_length=50, default="bi-table")
    
    # Upload do CSV (Apenas para importação inicial)
    arquivo_csv = models.FileField("Importar CSV", upload_to='dashboards/csv/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['csv'])])
    
    # Dados reais salvos no banco para edição
    cabecalhos = models.JSONField("Cabeçalhos da Tabela", default=list, blank=True)
    linhas_dados = models.JSONField("Dados das Linhas", default=list, blank=True)

    def save(self, *args, **kwargs):
        # Lógica para converter CSV em JSON no momento do salvamento
        if self.arquivo_csv and not self.linhas_dados:
            self.arquivo_csv.seek(0)
            decoded_file = self.arquivo_csv.read().decode('utf-8')
            reader = csv.reader(io.StringIO(decoded_file))
            data = list(reader)
            if data:
                self.cabecalhos = data[0] # Primeira linha é o cabeçalho
                self.linhas_dados = data[1:] # Restante são os dados
            self.arquivo_csv = None # Limpa o arquivo após importar
        super().save(*args, **kwargs)

class GraficoDinamico(models.Model):
    TIPO_GRAFICO =[
        ('bar', 'Gráfico de Barras (Bar)'),
        ('line', 'Gráfico de Linhas (Line)'),
        ('pie', 'Gráfico de Pizza (Pie)'),
        ('doughnut', 'Gráfico de Rosca (Doughnut)'),
    ]

    coluna = models.OneToOneField(Coluna, related_name='grafico', on_delete=models.CASCADE)
    titulo = models.CharField("Título do Gráfico", max_length=200)
    tipo = models.CharField("Tipo do Gráfico", max_length=20, choices=TIPO_GRAFICO, default='bar')
    
    arquivo_csv = models.FileField("Importar Dados via CSV", upload_to='dashboards/csv/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['csv'])])
    
    # Estrutura JSON padrão do Chart.js
    labels = models.JSONField("Rótulos (Eixo X)", default=list, blank=True)
    datasets = models.JSONField("Conjunto de Dados", default=list, blank=True)

    #No método save do GraficoDinamico:
    def save(self, *args, **kwargs):
        if self.arquivo_csv:
            self.arquivo_csv.seek(0)
            content = self.arquivo_csv.read().decode('utf-8')
            try:
                # Isso descobre se o arquivo usa , ou ; automaticamente
                dialect = csv.Sniffer().sniff(content[:1024])
                delimiter = dialect.delimiter
            except:
                delimiter = ',' 
                
            reader = csv.reader(io.StringIO(content), delimiter=delimiter)
            data = [row for row in list(reader) if any(row)]
            
            if len(data) > 1:
                headers = [h.strip() for h in data[0]]
                self.labels = [row[0].strip() for row in data[1:]]
                
                novos_datasets = []
                for i in range(1, len(headers)):
                    valores = []
                    for row in data[1:]:
                        # Trata números com vírgula (ex: 35,00 -> 35.00)
                        val = row[i].replace(',', '.').strip()
                        try:
                            valores.append(float(val))
                        except:
                            valores.append(0.0)
                    novos_datasets.append({"label": headers[i], "data": valores})
                self.datasets = novos_datasets
                self.arquivo_csv = None # Limpa o arquivo após processar
        super().save(*args, **kwargs)