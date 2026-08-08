# 🗄️ Manual 4: Criar Compose e Conectar ao Banco de Dados

Este manual ensina como subir uma nova aplicação (`app2`) e conectá-la ao banco de dados global (`meubanco_postgres`) usando comunicação direta na rede interna do Docker (sem expor o banco à internet).

## 1. Estrutura do Novo App
Crie a pasta da sua aplicação:
```bash
mkdir -p /srv/servidor_principal/apps/app_com_banco
cd /srv/servidor_principal/apps/app_com_banco
nano docker-compose.yml
```

## 2. O docker-compose.yml de exemplo
O segredo está em passar o nome do contêiner do banco (`meubanco_postgres`) nas variáveis de ambiente da sua aplicação.

```yaml
services:
  minha_aplicacao:
    image: minha_imagem_backend:latest # Ex: Node.js, Python, PHP, WordPress
    container_name: app_com_banco_container
    restart: always
    environment:
      # Credenciais do Banco de Dados
      - DB_HOST=meubanco_postgres   # <-- NOME DO CONTÊINER DO BANCO!
      - DB_PORT=5432
      - DB_NAME=postgres
      - DB_USER=postgres
      - DB_PASSWORD=senha_super_secreta
    networks:
      - rede_proxy                  # Obrigatório para achar o banco e o proxy

# Define a conexão com a rede global já existente
networks:
  rede_proxy:
    external: true
```

## 3. Subindo a Aplicação
Salve o arquivo e inicie a aplicação:
```bash
docker compose up -d
```

## 4. Como essa "Magia" funciona?
Como ambos os contêineres (o seu backend e o `meubanco_postgres`) estão na mesma rede (`rede_proxy`), o DNS embutido no Docker transforma a string `meubanco_postgres` diretamente no IP interno (ex: `172.18.0.x`). 
Isso garante latência zero na comunicação com o banco de dados, mantendo a porta `5432` fechada contra ataques externos.