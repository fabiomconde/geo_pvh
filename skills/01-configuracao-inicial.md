# 🛠️ Manual 1: Configuração Inicial do Servidor VPS

Este documento descreve os passos iniciais exigidos em um servidor VPS recém-formatado (Ubuntu 24.04 LTS) para prepará-lo para hospedar múltiplas aplicações Docker.

## 1. Configuração de DNS (Registro de Domínio)
Antes de configurar o servidor, aponte o seu domínio para o IP do VPS no painel de DNS da sua registradora (ex: Hostinger, Cloudflare).
- **Tipo A**: Nome `@` apontando para `IP_DO_VPS`
- **Tipo A (Wildcard)**: Nome `*` apontando para `IP_DO_VPS`
> *Nota: Remova registros AAAA (IPv6) legados para evitar falhas na emissão de certificados SSL.*

## 2. Acesso via SSH
No seu terminal local, acesse o servidor como root:
```bash
ssh root@IP_DO_VPS
```

## 3. Atualização e Instalação do Docker
Atualize a lista de pacotes do servidor e instale o Docker e o Docker Compose oficiais:
```bash
apt update && apt upgrade -y
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
systemctl enable --now docker
```

## 4. Permissões de Usuário
Para gerenciar o Docker sem precisar do comando `sudo` toda vez, adicione seu usuário (ex: `dev`) ao grupo do Docker:
```bash
sudo usermod -aG docker $USER
newgrp docker
```

## 5. Criação da Rede Global do Docker
Crie a rede virtual que conectará o Proxy Reverso a todas as aplicações do servidor:
```bash
docker network create rede_proxy
```