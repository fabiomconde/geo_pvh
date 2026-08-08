# 🤖 Manual 5: CI/CD com GitHub Actions e Ansible

Este documento descreve como a infraestrutura foi configurada para atualizar a aplicação em produção automaticamente sempre que houver um novo código na branch `main` (Integração e Entrega Contínuas - CI/CD).

## 1. Como Funciona a Automação?
1. O desenvolvedor faz um `git push` para o GitHub.
2. O **GitHub Actions** aloca um servidor temporário (Runner) e instala o **Ansible**.
3. O Ansible se conecta ao VPS via SSH e executa o "Ritual de Atualização" (Git Pull -> Build Docker -> Migrate).

## 2. Configuração das Chaves SSH (Segurança)
Para permitir que o GitHub acesse o servidor, criamos uma chave SSH dedicada:
\`\`\`bash
# No VPS:
ssh-keygen -t ed25519 -f ~/.ssh/github_actions_key -N ""
cat ~/.ssh/github_actions_key.pub >> ~/.ssh/authorized_keys
cat ~/.ssh/github_actions_key # Copia essa chave privada gerada
\`\`\`

No GitHub do projeto, acesse **Settings > Secrets and variables > Actions** e crie as variáveis:
* `VPS_SSH_KEY`: (A chave privada copiada)
* `VPS_IP`: (IP do servidor - ex: `2.25.184.18`)
* `VPS_USER`: (Usuário do servidor - ex: `dev`)

## 3. O Playbook do Ansible
No repositório do código, criamos o arquivo de instruções do deploy: `ansible/deploy.yml`
\`\`\`yaml
---
- name: Deploy da Aplicação no VPS
  hosts: all
  become: no  # Usuário já tem permissão de Docker
  vars:
    app_dir: /srv/servidor_principal/apps/rede_social/politica_intel
    repo_dir: /srv/servidor_principal/apps/rede_social

  tasks:
    - name: Atualizar código via Git Pull
      ansible.builtin.shell: git pull origin main
      args:
        chdir: "{{ repo_dir }}"

    - name: Reconstruir Imagem e Containeres (Sem downtime)
      ansible.builtin.shell: docker compose up -d --build
      args:
        chdir: "{{ app_dir }}"

    - name: Aplicar Migrações do Banco de Dados
      ansible.builtin.shell: docker exec app_politica_intel python manage.py migrate
      
    - name: Coletar Arquivos Estáticos
      ansible.builtin.shell: docker exec app_politica_intel python manage.py collectstatic --noinput
\`\`\`

## 4. O Fluxo do GitHub Actions
Na raiz do repositório, criamos o arquivo `.github/workflows/main.yml` que orquestra tudo, passando os "Segredos" como Variáveis de Ambiente para máxima segurança:

\`\`\`yaml
name: Deploy Automático VPS

on:
  push:
    branches:
      - main

jobs:
  deploy:
    name: Deploy com Ansible
    runs-on: ubuntu-latest

    steps:
      - name: Checkout do código
        uses: actions/checkout@v4

      - name: Instalar Ansible no Runner do GitHub
        run: sudo apt-get update && sudo apt-get install -y ansible

      - name: Preparar chaves SSH e Inventário
        env:
          PRIVATE_KEY: ${{ secrets.VPS_SSH_KEY }}
          IP_VPS: ${{ secrets.VPS_IP }}
          USUARIO_VPS: ${{ secrets.VPS_USER }}
        run: |
          mkdir -p ~/.ssh
          echo "$PRIVATE_KEY" > ~/.ssh/id_rsa
          chmod 600 ~/.ssh/id_rsa
          
          # Cria o inventário para o Ansible
          echo "$IP_VPS ansible_user=$USUARIO_VPS" > inventory.ini

      - name: Executar o Ansible Playbook
        env:
          ANSIBLE_HOST_KEY_CHECKING: False # Ignora known_hosts para evitar falhas do keyscan
        run: ansible-playbook -i inventory.ini ansible/deploy.yml --private-key ~/.ssh/id_rsa
\`\`\`

> **Resultado:** Qualquer alteração no código agora é enviada ao VPS, reconstruída, e migrada de forma 100% automatizada em menos de 1 minuto.