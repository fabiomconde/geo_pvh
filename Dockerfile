FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    gdal-bin libgdal-dev libgeos-dev libproj-dev \
    postgresql-client gcc g++ python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia o requirements da RAIZ do projeto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o CONTEÚDO da pasta django_app para a pasta /app do container
COPY django_app/ . 

RUN mkdir -p /app/staticfiles /app/media
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

EXPOSE 8000

# Verifique se o nome da pasta interna onde está o wsgi.py é 'core' 
# Se for outro nome, mude 'core.wsgi:application' abaixo
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]