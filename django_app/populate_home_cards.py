import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from core_gis.models import SecaoHome, CardSecao

def populate_home():
    print("⏳ Deletando seções existentes para evitar duplicidade...")
    SecaoHome.objects.all().delete()
    
    print("🚀 Iniciando população de Seções e Cards na Home...")

    # =========================================================================
    # 1. Seção: PUBLICAÇÕES
    # =========================================================================
    secao_pub = SecaoHome.objects.create(
        titulo="Publicações",
        subtitulo="Veja as publicações e estudos realizados",
        icone="clipboard-edit.svg",
        tipo="publicacao",
        cor_fundo="var(--theme-bg-publicacoes)",
        ordem=1
    )
    
    CardSecao.objects.create(
        secao=secao_pub,
        titulo="Conflitos Socioambientais",
        subtitulo="Publicações de artigos acadêmicos sobre conflitos socioambientais.",
        url="?tipo=10",
        icone="alert-triangle.svg",
        texto_botao="Acessar Artigos Acadêmicos",
        btn_class="btn-primary",
        badge_text="Artigo Acadêmico",
        badge_class="theme-docs",
        ordem=1
    )
    
    CardSecao.objects.create(
        secao=secao_pub,
        titulo="Nota Pública",
        subtitulo="Publicações de notas públicas.",
        url="?tipo=8",
        icone="book-open.svg",
        texto_botao="Acessar Notas Públicas",
        btn_class="btn-primary",
        badge_text="Nota Pública",
        badge_class="theme-docs",
        ordem=2
    )
    
    CardSecao.objects.create(
        secao=secao_pub,
        titulo="Relatório Técnico",
        subtitulo="Publicações de relatórios técnicos.",
        url="?tipo=7",
        icone="clipboard-list.svg",
        texto_botao="Acessar Relatórios Técnicos",
        btn_class="btn-primary",
        badge_text="Relatório Técnico",
        badge_class="theme-docs",
        ordem=3
    )

    # =========================================================================
    # 2. Seção: DASHBOARDS
    # =========================================================================
    secao_dash = SecaoHome.objects.create(
        titulo="Dashboards",
        subtitulo="Analise dados e estatísticas através de gráficos interativos",
        icone="chart-line.svg",
        tipo="dashboard",
        cor_fundo="var(--theme-bg-white)",
        ordem=2
    )

    CardSecao.objects.create(
        secao=secao_dash,
        titulo="Dashboard de Desmatamento",
        subtitulo="Análise temporal e espacial do desmatamento.",
        url="core_gis:dashboard_prodes",
        icone="chart-line-up.svg",
        texto_botao="Acessar Dashboard",
        btn_class="btn-primary",
        badge_text="PRODES",
        badge_class="theme-forest",
        ordem=1
    )

    CardSecao.objects.create(
        secao=secao_dash,
        titulo="Dashboard de Alertas",
        subtitulo="Acompanhamento dos alertas de alteração na cobertura florestal.",
        url="core_gis:dashboard_deter",
        icone="chart-line-down.svg",
        texto_botao="Acessar Dashboard",
        btn_class="btn-primary",
        badge_text="DETER",
        badge_class="theme-alert",
        ordem=2
    )

    CardSecao.objects.create(
        secao=secao_dash,
        titulo="Dashboard de Focos",
        subtitulo="Análise de focos de calor em áreas de vegetação nativa e desmatamento.",
        url="core_gis:dashboard_focos",
        icone="fire.svg",
        texto_botao="Acessar Dashboard",
        btn_class="btn-primary",
        badge_text="QUEIMADAS",
        badge_class="theme-fire",
        ordem=3
    )

    # =========================================================================
    # 3. Seção: MAPAS INTERATIVOS
    # =========================================================================
    secao_mapas = SecaoHome.objects.create(
        titulo="Mapas Interativos",
        subtitulo="Visualize os dados geográficos de Porto Velho em mapas interativos",
        icone="map.svg",
        tipo="mapa",
        cor_fundo="var(--theme-bg-maps)",
        ordem=3
    )

    CardSecao.objects.create(
        secao=secao_mapas,
        titulo="Mapa de Desmatamento",
        subtitulo="Visualize os polígonos de supressão de vegetação nativa detectados pelo programa PRODES/INPE para Porto Velho.",
        url="core_gis:mapa_desmatamento",
        icone="tree.svg",
        texto_botao="Acessar Mapa",
        btn_class="btn-primary",
        badge_text="PRODES",
        badge_class="theme-forest",
        ordem=1
    )

    CardSecao.objects.create(
        secao=secao_mapas,
        titulo="Mapa de Alertas",
        subtitulo="Acompanhe os alertas de alteração na cobertura florestal detectados em tempo quase real pelo sistema DETER.",
        url="core_gis:mapa_alertas",
        icone="alert-triangle.svg",
        texto_botao="Acessar Mapa",
        btn_class="btn-primary",
        badge_text="DETER",
        badge_class="theme-alert",
        ordem=2
    )

    CardSecao.objects.create(
        secao=secao_mapas,
        titulo="Mapa de Focos de Calor",
        subtitulo="Monitore os focos de calor detectados por satélites na região de Porto Velho e entorno.",
        url="core_gis:mapa_focos",
        icone="fire.svg",
        texto_botao="Acessar Mapa",
        btn_class="btn-primary",
        badge_text="QUEIMADAS",
        badge_class="theme-fire",
        ordem=3
    )

    print("✅ Seções e Cards Iniciais populados no banco de dados com sucesso!")

if __name__ == '__main__':
    populate_home()
