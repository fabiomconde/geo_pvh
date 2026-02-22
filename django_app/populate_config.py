from core_gis.models import Configuracao

sobre_html = """
<div class="card mb-4">
    <div class="card-body">
        <h5 class="card-title">O que é o Observatório de Conflitos Socioambientais e Direitos Humanos -
            Porto Velho?</h5>
        <p class="card-text">
            O Observatório de Conflitos Socioambientais e Direitos Humanos - Porto Velho é uma plataforma
            com objetivo implementar um Observatório que integre
            monitoramento territorial, formação engajada e produção de subsídios para políticas públicas.
        </p>
        <p class="card-text">
            Enquanto Objetivos Específicos, pretendemos: i) Produzir um diagnóstico socioambiental
            atualizado relacionado ao recorte espacial definido para a Linha 1 de financiamento; ii)
            Desenvolver metodologias participativas para a gestão territorial municipal; iii) Implementar
            um modelo de curricularização da extensão em nível de graduação e pós-graduação em âmbito
            da unidade executora, considerando o Planejamento Participativo enquanto prática e método;
            iv) Estruturar uma plataforma digital permanente que subsidie diretamente o Observatório, na
            qual este instrumento será operacionalizado; v) Produzir subsídios técnicos para incidência
            política.
        </p>
        <p class="card-text">
            A plataforma integra dados geográficos com banco de dados municipais para gestão do território e
            acesso universal
        </p>
    </div>
</div>

<div class="card mb-4">
    <div class="card-body">
        <h5 class="card-title">Funcionalidades</h5>
        <ul class="list-unstyled">
            <li class="mb-2">
                <i class="bi bi-check-circle text-success"></i>
                <strong>Mapas Interativos:</strong> Visualização de dados geográficos com Leaflet
            </li>
            <li class="mb-2">
                <i class="bi bi-check-circle text-success"></i>
                <strong>Dashboards:</strong> Gráficos e estatísticas com Chart.js
            </li>
            <li class="mb-2">
                <i class="bi bi-check-circle text-success"></i>
                <strong>Web Services:</strong> Acesso via WMS, WFS para integração GIS
            </li>
            <li class="mb-2">
                <i class="bi bi-check-circle text-success"></i>
                <strong>API REST:</strong> Dados em formato GeoJSON para desenvolvedores
            </li>
            <li class="mb-2">
                <i class="bi bi-check-circle text-success"></i>
                <strong>Downloads:</strong> Arquivos em formato shapefile e GeoJSON
            </li>
        </ul>
    </div>
</div>

<div class="card mb-4">
    <div class="card-body">
        <h5 class="card-title">Tecnologias Utilizadas</h5>
        <div class="row">
            <div class="col-md-6">
                <ul class="list-unstyled">
                    <li><i class="bi bi-gear text-primary"></i> Django + GeoDjango</li>
                    <li><i class="bi bi-database text-primary"></i> PostgreSQL + PostGIS</li>
                    <li><i class="bi bi-globe text-primary"></i> GeoServer (WMS/WFS)</li>
                </ul>
            </div>
            <div class="col-md-6">
                <ul class="list-unstyled">
                    <li><i class="bi bi-map text-primary"></i> Leaflet.js</li>
                    <li><i class="bi bi-bar-chart text-primary"></i> Chart.js</li>
                    <li><i class="bi bi-server text-primary"></i> Redis + Nginx</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<div class="card">
    <div class="card-body">
        <h5 class="card-title">Fontes de Dados</h5>
        <ul>
            <li><a href="http://terrabrasilis.dpi.inpe.br" target="_blank">TerraBrasilis - INPE</a></li>
            <li><a href="http://www.obt.inpe.br/OBT/assuntos/programas/amazonia/prodes"
                    target="_blank">PRODES - Programa de Cálculo do Desflorestamento da Amazônia</a></li>
            <li><a href="http://www.obt.inpe.br/OBT/assuntos/programas/amazonia/deter" target="_blank">DETER
                    - Sistema de Detecção do Desmatamento em Tempo Real</a></li>
            <li><a href="https://queimadas.dgi.inpe.br" target="_blank">Programa Queimadas - INPE</a></li>
        </ul>
    </div>
</div>
"""

mensagem_inicio_html = """
<h1 class="hero-title">
    <span class="icon-svg"
        style="-webkit-mask-image: url(/static/images/regular/eye-scan.svg); mask-image: url(/static/images/regular/eye-scan.svg);"></span>
    Conflitos Socioambientais e Direitos Humanos - Porto Velho
</h1>
<p class="hero-subtitle">
    Plataforma digital de monitoramento e divulgação científica focada em Porto Velho
</p>
<p class="hero-description">
    Acesse, consulte e analise dados espaciais sobre conflitos socioambientais e direitos humanos
    e outras informações do município de Porto Velho.
</p>
"""

rodape_informativo_html = """
<div class="row">
    <div class="col-md-4">
        <h5><i class="bi bi-link-45deg"></i> Links</h5>
        <ul class="footer-links">
            <li><a href="https://www.gov.br/inpe" target="_blank">INPE</a></li>
            <li><a href="https://terrabrasilis.dpi.inpe.br" target="_blank">TerraBrasilis</a></li>
            <li><a href="http://www.obt.inpe.br/OBT/assuntos/programas/amazonia/prodes"
                    target="_blank">PRODES</a></li>
            <li><a href="http://www.obt.inpe.br/OBT/assuntos/programas/amazonia/deter"
                    target="_blank">DETER</a></li>
            <li><a href="https://portovelho.ro.gov.br" target="_blank">Protótipo de Observatório Geoespacial
                    de Porto Velho - Rondônia</a></li>
        </ul>
    </div>
    <div class="col-md-4">
        <h5><i class="bi bi-geo-alt"></i> Contato</h5>
        <address>
            <p><i class="bi bi-building"></i> Protótipo de Observatório Geoespacial de Porto Velho -
                Rondônia</p>
            <p><i class="bi bi-pin-map"></i> BR</p>
            <p><i class="bi bi-geo"></i> Porto Velho - RO</p>
        </address>
    </div>
    <div class="col-md-4">
        <h5><i class="bi bi-info-circle"></i> Sobre</h5>
        <p>
            Observatório de Conflitos Socioambientais e Direitos Humanos é uma plataforma de dados
            geográficos
            para monitoramento ambiental e territorial do município.
        </p>
        <p class="license">
            <i class="bi bi-cc-circle"></i>
            Dados sob licença Creative Commons CC BY-NC-SA 4.0
        </p>
    </div>
</div>
"""

Configuracao.objects.update_or_create(identificador="sobre", defaults={"corpo_texto": sobre_html})
Configuracao.objects.update_or_create(identificador="mensagem_inicio", defaults={"corpo_texto": mensagem_inicio_html})
Configuracao.objects.update_or_create(identificador="rodape_informativo", defaults={"corpo_texto": rodape_informativo_html})
print("Configurações iniciais carregadas!")
