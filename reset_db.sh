#!/bin/bash

# Configuration
MODULE="core_gis"
DB_CONTAINER="db"
DB_USER="geouser"
DB_NAME="pvh_geoportal"
DJANGO_CONTAINER="django"

echo "=================================================="
echo "⚠️  ATENÇÃO: Este script irá DESTRUIR o banco de dados"
echo "e REFAZER todas as migrações do zero."
echo "=================================================="

# 1. Excluir os arquivos de migração (exceto __init__.py)
echo "[1/6] 🗑️  Excluindo arquivos de migração antigos do módulo '$MODULE'..."
docker compose -f docker-compose_dev.yml exec -T $DJANGO_CONTAINER bash -c "find $MODULE/migrations -type f -not -name '__init__.py' -delete"
docker compose -f docker-compose_dev.yml exec -T $DJANGO_CONTAINER bash -c "find $MODULE/migrations -type d -name '__pycache__' -exec rm -rf {} +"

# 2. Excluir os schemas e recriar
echo "[2/6] 💥 Removendo esquemas 'public' e 'geo' e recriando para um reset total..."
docker compose -f docker-compose_dev.yml exec -T $DB_CONTAINER psql -U $DB_USER -d $DB_NAME -c "
DROP SCHEMA IF EXISTS public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO $DB_USER;
GRANT ALL ON SCHEMA public TO public;

DROP SCHEMA IF EXISTS geo CASCADE;
CREATE SCHEMA geo;
GRANT ALL ON SCHEMA geo TO $DB_USER;
GRANT ALL ON SCHEMA geo TO public;

CREATE EXTENSION IF NOT EXISTS postgis;
"

# 2.1 Rodar init_db.sql para criar esquemas geoestaciais necessários antes de aplicar o migrate
echo "[2.1/6] 🏗️ Construindo o banco com init_db.sql..."
docker compose -f docker-compose_dev.yml exec -T db psql -U $DB_USER -d $DB_NAME -f /docker-entrypoint-initdb.d/init_db.sql

# 3. Criar novas migrações
echo "[3/6] 📦 Criando novas migrações (makemigrations)..."
docker compose -f docker-compose_dev.yml exec -T $DJANGO_CONTAINER python manage.py makemigrations $MODULE
docker compose -f docker-compose_dev.yml exec -T $DJANGO_CONTAINER python manage.py makemigrations

# 4. Aplicar migrações
echo "[4/6] 🚀 Aplicando migrações (migrate)..."
docker compose -f docker-compose_dev.yml exec -T $DJANGO_CONTAINER python manage.py migrate

# 4.1 Criar superuser admin / admin
echo "[4.1/6] 👤 Criando superuser..."
docker compose -f docker-compose_dev.yml exec -T $DJANGO_CONTAINER python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')"

# 5. Popular o banco com scripts raiz (se aplicável ao ambiente do user. O user pediu import_ibge_setores, import_shapes e popular_banco_publicacoes)
echo "[5/6] 📊 Executando comandos de importação e população de banco..."
echo "-> Importando Setores IBGE..."
docker compose -f docker-compose_dev.yml exec -T $DJANGO_CONTAINER python manage.py import_ibge_setores
echo "-> Importando Shapes..."
docker compose -f docker-compose_dev.yml exec -T $DJANGO_CONTAINER python manage.py import_shapes
echo "-> Populando Banco Principal..."
docker compose -f docker-compose_dev.yml exec -T $DJANGO_CONTAINER python manage.py popular_banco_publicacoes

# 6. Rodar scripts soltos criados anteriormente (ex: config, secões da home)
echo "[6/6] 📝 Rodando os scripts de conteúdo do site..."
docker compose -f docker-compose_dev.yml exec -T $DJANGO_CONTAINER python populate_config.py
docker compose -f docker-compose_dev.yml exec -T $DJANGO_CONTAINER python populate_home_cards.py

echo "=================================================="
echo "✅ Processo de reset do banco e populações concluído!"
echo "=================================================="
