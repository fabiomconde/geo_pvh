# 🌐 Manual 3: Adição de Aplicações no Proxy Reverso (NPM)

O **Nginx Proxy Manager** é a porta de entrada da nossa infraestrutura. Ele recebe requisições (ex: `app1.dominio.com`) e roteia internamente para o contêiner correspondente (`app1_container`), além de gerenciar certificados SSL gratuitos.

## 1. Subindo a Aplicação
Sempre verifique se a sua aplicação no `docker-compose.yml` está conectada à rede correta:
```yaml
    networks:
      - rede_proxy
```
*(Levante a aplicação usando `docker compose up -d`)*

## 2. Acessando o Painel do Proxy
Acesse no seu navegador: `http://IP_DO_VPS:81`
*(Faça login com seu e-mail e senha administrativa)*

## 3. Configurando a Rota (Proxy Host)
1. Acesse **Hosts** > **Proxy Hosts** > **Add Proxy Host**.
2. Na aba **Details**:
   - **Domain Names**: O subdomínio desejado (ex: `app1.provaconceito.tech`) -> *Pressione Enter!*
   - **Scheme**: `http`
   - **Forward Hostname / IP**: O `container_name` exato do seu serviço no Docker (ex: `app1_container`). O Docker resolverá o IP sozinho!
   - **Forward Port**: A porta interna da sua aplicação (ex: `80`, `3000`, `8080`).
   - **Block Common Exploits**: Marcado.

## 4. Gerando o Cadeado Verde (SSL)
1. Sem fechar a janela, clique na aba **SSL**:
   - Mude "SSL Certificate" para **Request a new SSL Certificate**.
   - Marque as caixas **Force SSL** e **HTTP/2 Support**.
   - Confirme seu e-mail e concorde com os termos da Let's Encrypt.
   - Clique em **Save**.

Aguarde alguns segundos. A aplicação já está online, protegida e mapeada no seu subdomínio!