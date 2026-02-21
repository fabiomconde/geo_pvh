import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from core_gis.models import (
    TipoDocumento, FaseConflito, TipoTerritorio, Bioma, TipoAtor,
    PapelAtor, SetorEconomico, DireitoAfetado, TipoViolacao,
    Localizacao, Ator, Conflito, EnvolvimentoAtor, Publicacao
)

fake = Faker('pt_BR')

class Command(BaseCommand):
    help = 'Popula o banco com dados massivos (50+ posts, 8 conflitos) em Porto Velho/RO'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Iniciando população massiva...'))

        with transaction.atomic():
            # 1. Limpeza
            self.limpar_banco()

            # 2. Taxonomias Base
            taxonomias = self.criar_taxonomias()
            
            # 3. Atores e Locais
            atores = self.criar_atores(taxonomias)
            locais = self.criar_localizacoes(taxonomias)

            # 4. Criação dos Conflitos
            conflitos = self.criar_conflitos(taxonomias, atores, locais)

            # 5. Criação das Publicações
            self.criar_publicacoes(conflitos, taxonomias, atores)

        self.stdout.write(self.style.SUCCESS('Script finalizado com sucesso!'))

    def limpar_banco(self):
        self.stdout.write('Limpando dados antigos...')
        Publicacao.objects.all().delete()
        EnvolvimentoAtor.objects.all().delete()
        Conflito.objects.all().delete()
        # Não deletamos atores/taxonomias para não quebrar integridade se o script rodar parcial
        # Mas em ambiente de dev limpo, pode descomentar:
        # Ator.objects.all().delete()
        # Localizacao.objects.all().delete()

    def criar_taxonomias(self):
        self.stdout.write('Gerando taxonomias...')
        
        bioma_amz, _ = Bioma.objects.get_or_create(nome="Amazônia")
        Bioma.objects.get_or_create(nome="Cerrado")

        docs = ["Notícia", "Relatório Técnico", "Nota Pública", "Decisão Judicial", "Artigo Acadêmico"]
        objs_docs = [TipoDocumento.objects.get_or_create(nome=d)[0] for d in docs]

        fases = ["Latente", "Em Negociação", "Conflito Aberto", "Judicializado"]
        objs_fases = [FaseConflito.objects.get_or_create(nome=f)[0] for f in fases]

        viols = [
            "Contaminação por Mercúrio", "Grilagem de Terras", "Trabalho Escravo",
            "Ameaça de Morte", "Desmatamento Ilegal", "Invasão de Território"
        ]
        objs_viols = [TipoViolacao.objects.get_or_create(nome=v)[0] for v in viols]

        return {
            'bioma_amz': bioma_amz,
            'docs': objs_docs,
            'fases': objs_fases,
            'violacoes': objs_viols,
            'setor_min': SetorEconomico.objects.get_or_create(nome="Mineração")[0],
            'setor_agro': SetorEconomico.objects.get_or_create(nome="Agronegócio/Pecuária")[0],
            'setor_hidro': SetorEconomico.objects.get_or_create(nome="Hidrelétricas")[0],
            'tipo_ti': TipoTerritorio.objects.get_or_create(nome="Terra Indígena")[0],
            'tipo_uc': TipoTerritorio.objects.get_or_create(nome="Unidade de Conservação")[0],
            'tipo_urb': TipoTerritorio.objects.get_or_create(nome="Área Urbana")[0],
            'papel_vitima': PapelAtor.objects.get_or_create(nome="Vítima/Atingido")[0],
            'papel_reu': PapelAtor.objects.get_or_create(nome="Causador/Réu")[0],
            'papel_fiscal': PapelAtor.objects.get_or_create(nome="Fiscalizador")[0], # Adicionado para evitar erro lógico
        }

    def criar_localizacoes(self, tax):
        # Usamos get_or_create para evitar duplicar se rodar 2x
        locais_data = [
            ("TI Karipuna", "Porto Velho", "RO", tax['tipo_ti'], -9.15, -64.50),
            ("RESEX Jaci-Paraná", "Porto Velho", "RO", tax['tipo_uc'], -9.45, -64.38),
            ("Distrito de Mutum-Paraná", "Porto Velho", "RO", tax['tipo_urb'], -9.61, -64.83),
            ("Rio Madeira (Baixo)", "Porto Velho", "RO", tax['tipo_uc'], -8.75, -63.88),
            ("União Bandeirantes", "Porto Velho", "RO", tax['tipo_urb'], -9.82, -64.21),
        ]
        lista = []
        for nome, mun, uf, tipo, lat, lon in locais_data:
            obj, _ = Localizacao.objects.get_or_create(
                nome_territorio=nome,
                defaults={'municipio': mun, 'estado': uf, 'tipo': tipo, 'bioma': tax['bioma_amz'], 'latitude': lat, 'longitude': lon}
            )
            lista.append(obj)
        return lista

    def criar_atores(self, tax):
        # Atores fixos para garantir coerência
        atores_data = [
            ("Consórcio Madeira Energia", tax['setor_hidro']),      # 0
            ("Cooperativa de Garimpeiros", tax['setor_min']),       # 1
            ("Madeireira Ypê (Fictícia)", tax['setor_agro']),       # 2
            ("Associação do Povo Karipuna", None),                  # 3
            ("CPT - Comissão Pastoral da Terra", None),             # 4
            ("MPF - Ministério Público Federal", None),             # 5
            ("IBAMA", None),                                        # 6
            ("Associação de Moradores de Jaci", None),              # 7
        ]
        
        lista_atores = []
        tipo_geral, _ = TipoAtor.objects.get_or_create(nome="Geral")
        
        for nome, setor in atores_data:
            ator, _ = Ator.objects.get_or_create(
                nome=nome,
                defaults={'tipo': tipo_geral, 'setor_economico': setor, 'historico': "<p>Descrição gerada automaticamente.</p>"}
            )
            lista_atores.append(ator)
        
        return lista_atores

    def criar_conflitos(self, tax, atores, locais):
        self.stdout.write('Criando conflitos...')
        
        cenarios = [
            ("Invasão na TI Karipuna", "Madeireiros invadem área.", tax['setor_agro']),
            ("Contaminação Mercúrio Madeira", "Garimpo afeta saúde.", tax['setor_min']),
            ("Cheias em Jaci-Paraná", "Impacto das barragens.", tax['setor_hidro']),
            ("Desmatamento União Bandeirantes", "Pecuária ilegal.", tax['setor_agro']),
            ("Conflito Ponta do Abunã", "Disputa de terras.", tax['setor_agro']),
            ("Pesca Predatória RESEX", "Barcos industriais.", tax['setor_min']),
            ("Assoreamento Igarapé", "Obras urbanas.", tax['setor_hidro']),
            ("Ameaças Mutum-Paraná", "Violência no campo.", tax['setor_agro']),
        ]

        lista_conflitos = []
        
        for titulo, resumo, setor in cenarios:
            c, created = Conflito.objects.get_or_create(
                nome=titulo,
                defaults={
                    'resumo': resumo,
                    'historico_completo': f"<h2>Histórico</h2><p>{fake.text()}</p>",
                    'fase_atual': random.choice(tax['fases']),
                    'data_inicio': fake.date_between(start_date='-10y', end_date='-5y'),
                }
            )
            
            c.localizacoes.add(random.choice(locais))
            
            # --- CORREÇÃO DO ERRO AQUI ---
            # Usamos get_or_create para evitar UniqueViolation
            
            # 1. MPF como Fiscal (Índice 5)
            EnvolvimentoAtor.objects.get_or_create(
                conflito=c, 
                ator=atores[5], 
                defaults={'papel': tax['papel_fiscal']}
            )

            # 2. Causador (Indices 0 a 2)
            EnvolvimentoAtor.objects.get_or_create(
                conflito=c, 
                ator=random.choice(atores[:3]), 
                defaults={'papel': tax['papel_reu']}
            )
            
            # 3. Vítima (Indices 3, 4, 7 - Evitamos o MPF/IBAMA aqui para lógica fazer sentido)
            vitimas_possiveis = [atores[3], atores[4], atores[7]]
            EnvolvimentoAtor.objects.get_or_create(
                conflito=c, 
                ator=random.choice(vitimas_possiveis), 
                defaults={'papel': tax['papel_vitima']}
            )
            
            lista_conflitos.append(c)

        return lista_conflitos

    def criar_publicacoes(self, conflitos, tax, atores):
        self.stdout.write(f'Gerando publicações...')
        
        count = 0
        while count < 55:
            conflito = random.choice(conflitos)
            
            p = Publicacao.objects.create(
                titulo=f"Notícia {count}: {fake.sentence()}",
                subtitulo=fake.sentence(),
                tipo_documento=random.choice(tax['docs']),
                corpo_texto=f"<p>{fake.paragraph()}</p>",
                conflito=conflito,
                data_publicacao=timezone.now(),
                is_publicado=True
            )
            
            # Add ManyToMany
            p.atores_citados.add(random.choice(atores))
            p.violacoes_denunciadas.add(random.choice(tax['violacoes']))
            
            count += 1
            if count % 10 == 0:
                self.stdout.write(f'... {count} criadas')