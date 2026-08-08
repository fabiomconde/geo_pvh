# 📂 Manual 2: Arquitetura e Segurança do Servidor

Para garantir que o servidor seja imune a acessos indevidos e fácil de migrar, nossa infraestrutura utiliza o Firewall UFW (Uncomplicated Firewall) como escudo externo e a pasta `/srv` como coração do sistema.

## 1. Camada de Segurança (Firewall UFW)
O Ubuntu possui um firewall nativo que bloqueia todas as portas por padrão. Vamos abri-lo apenas para o tráfego essencial (SSH, Web e o Painel do Proxy).

No terminal do servidor, execute:
\`\`\`bash
# 1. Garante que você não será bloqueado de acessar o servidor
sudo ufw allow OpenSSH

# 2. Libera o tráfego Web normal (Nginx)
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 3. Libera a porta de administração do Nginx Proxy Manager
sudo ufw allow 81/tcp

# 4. Ativa o Firewall (Pressione 'y' para confirmar)
sudo ufw enable
\`\`\`
> **⚠️ Regra de Ouro do Docker:** O Docker pode ignorar o UFW se você usar a diretiva `ports` no `docker-compose.yml`. Por isso, **NUNCA** usamos `ports: ["5432:5432"]` no banco de dados. Ele se comunica apenas pela rede interna (`rede_proxy`), ficando 100% invisível para a internet externa.

## 2. O Diretório Mestre (/srv)
A raiz do nosso ambiente de serviços é: `/srv/servidor_principal`

### Árvore de Diretórios:
\`\`\`text
/srv/servidor_principal/
│
├── infra/                  # Serviços essenciais do servidor
│   ├── proxy/              # Nginx Proxy Manager (Roteamento e SSL)
│   └── banco/              # PostgreSQL + pgAdmin (Dados)
│
└── apps/                   # Aplicações conteinerizadas
    ├── rede_social/        # Código do GitHub (Django + Redis)
    └── site_principal/     # Página estática HTML (Nginx)
\`\`\`

## 3. Criando e Configurando o Diretório
Garantimos que a pasta pertença ao usuário padrão (ex: `dev`), para facilitar deploys automáticos sem a necessidade de permissões `root`:
\`\`\`bash
sudo mkdir -p /srv/servidor_principal/{infra,apps}
sudo chown -R $USER:$USER /srv/servidor_principal
\`\`\`

## 4. Estratégia de Migração Rápida
Como os `docker-compose.yml` usam volumes relativos (ex: `./pgdata:/var/lib/postgresql`), todos os dados (incluindo o banco de dados) vivem na mesma pasta dos arquivos de configuração.
Para migrar de VPS, basta compactar a pasta (`tar -czvf backup.tar.gz /srv/servidor_principal`), enviar para a máquina nova e subir os containers novamente.