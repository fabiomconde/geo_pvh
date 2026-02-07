# Observatório de Conflitos Socioambientais e Direitos Humanos Porto Velho

Sistema de Informação Geográfica (SIG) para monitoramento ambiental e territorial do município de Porto Velho, Rondônia.

Desenvolvido com arquitetura similar ao [TerraBrasilis](https://terrabrasilis.dpi.inpe.br/).

## Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                           NGINX                                  │
│                    (Reverse Proxy :80)                          │
└───────────────────────┬───────────────────────┬─────────────────┘
                        │                       │
                        ▼                       ▼
┌─────────────────────────────┐   ┌─────────────────────────────┐
│        DJANGO               │   │        GEOSERVER            │
│   (GeoDjango + DRF :8000)   │   │      (WMS/WFS :8080)        │
└──────────────┬──────────────┘   └──────────────┬──────────────┘
               │                                  │
               ▼                                  │
┌─────────────────────────────┐                  │
│          REDIS              │                  │
│        (Cache :6379)        │                  │
└─────────────────────────────┘                  │
                                                 │
               ┌─────────────────────────────────┘
               ▼
┌─────────────────────────────────────────────────────────────────┐
│                         PostgreSQL + PostGIS                     │
│                          (Database :5432)                        │
└─────────────────────────────────────────────────────────────────┘
```

## Funcionalidades

### Mapas Interativos
- **PRODES**: Mapa de desmatamento com polígonos de supressão de vegetação
- **DETER**: Mapa de alertas de alteração na cobertura florestal
- **Focos de Calor**: Mapa de queimadas detectadas por satélites

### Dashboards
- Gráficos de evolução temporal do desmatamento
- Estatísticas por ano, classe e período
- Indicadores de monitoramento ambiental

### Acesso a Dados
- Downloads em formato GeoJSON e Shapefile
- Web Services (WMS/WFS) compatíveis com INDE/OGC
- API REST com suporte a GeoJSON

## Requisitos

- Docker e Docker Compose
- 4GB+ RAM
- 10GB+ espaço em disco

## Instalação e Execução

### 1. Clone o repositório
```bash
git clone <repository-url>
cd pvh_geoportal
```

### 2. Configure as variáveis de ambiente
```bash
cp .env.example .env
# Edite o arquivo .env conforme necessário
```

### 3. Inicie os containers
```bash
docker-compose up -d
```

### 4. Aguarde a inicialização
```bash
# Verifique os logs
docker-compose logs -f

# Verifique o status dos containers
docker-compose ps
```

### 5. Acesse os serviços
- **Portal Web**: http://localhost
- **Django Admin**: http://localhost/admin
- **GeoServer**: http://localhost/geoserver
- **API REST**: http://localhost/api

## Estrutura do Projeto

```
pvh_geoportal/
├── docker-compose.yml       # Orquestração dos containers
├── .env                     # Variáveis de ambiente
├── data_source/             # Dados de mapas
│   ├── shapes_bairros/      # Shapefiles de bairros
│   ├── shapes_desmatamento/ # Dados PRODES/INPE
│   └── geojson_import/      # Arquivos temporários
├── django_app/              # Aplicação Django
│   ├── core/                # Configurações Django
│   ├── core_gis/            # App principal GeoDjango
│   │   ├── models.py        # Modelos geográficos
│   │   ├── views.py         # Views e APIs
│   │   ├── api/             # Django REST Framework
│   │   └── management/      # Comandos de importação
│   ├── static/              # CSS, JS, imagens
│   └── templates/           # Templates HTML
├── geoserver_data/          # Dados do GeoServer
├── nginx/                   # Configuração Nginx
├── redis_data/              # Dados do Redis
└── scripts/                 # Scripts auxiliares
    └── init_db.sql          # Inicialização do banco
```

## Importação de Dados

### Importar Shapefiles do PRODES
```bash
# Acesse o container Django
docker-compose exec django bash

# Execute o comando de importação
python manage.py import_shapes --shapefile /app/data_source/shapes_desmatamento/arquivo.shp --type desmatamento
```

### Importar dados via SQL
```bash
# Acesse o container do banco
docker-compose exec db psql -U geouser -d pvh_geoportal

# Execute o comando shp2pgsql
shp2pgsql -s 4674 -I -W "latin1" arquivo.shp public.prodes_raw | psql -h localhost -U geouser -d pvh_geoportal
```

## API REST

### Endpoints Disponíveis

| Endpoint | Descrição |
|----------|-----------|
| `/api/desmatamento/` | Dados de desmatamento PRODES |
| `/api/alertas/` | Alertas DETER |
| `/api/focos/` | Focos de calor |
| `/api/bairros/` | Bairros de Porto Velho |
| `/api/municipios/` | Municípios de Rondônia |

### Exemplos de Uso

```python
import requests

# Listar desmatamento por ano
response = requests.get('http://localhost/api/desmatamento/?ano=2023')
data = response.json()

# Obter GeoJSON
response = requests.get('http://localhost/api/desmatamento/?format=json')
geojson = response.json()
```

## Web Services

### WMS (Web Map Service)
```
URL: http://localhost/geoserver/pvh/wms
Camadas: pvh:desmatamento_pvh, pvh:alertas_deter, pvh:focos_calor
```

### WFS (Web Feature Service)
```
URL: http://localhost/geoserver/pvh/wfs
Formatos: GeoJSON, GML, Shapefile, KML
```

## Tecnologias

- **Backend**: Django 4.2, GeoDjango, Django REST Framework
- **Database**: PostgreSQL 15 + PostGIS 3.3
- **Map Server**: GeoServer 2.23
- **Cache**: Redis 7
- **Proxy**: Nginx
- **Frontend**: Bootstrap 5, Leaflet.js, Chart.js

## Fontes de Dados

- [PRODES/INPE](http://www.obt.inpe.br/OBT/assuntos/programas/amazonia/prodes)
- [DETER/INPE](http://www.obt.inpe.br/OBT/assuntos/programas/amazonia/deter)
- [TerraBrasilis](https://terrabrasilis.dpi.inpe.br/)
- [Programa Queimadas](https://queimadas.dgi.inpe.br/)

## Licença

Dados sob licença [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
