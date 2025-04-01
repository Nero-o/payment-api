FROM python:3.11-slim

# Configurar variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY . .

# Tornar o script de entrypoint executável
RUN chmod +x /app/scripts/docker_entrypoint.sh

# Definir o entrypoint
ENTRYPOINT ["/app/scripts/docker_entrypoint.sh"]

# Expor a porta da aplicação
EXPOSE 8000

# Comando para executar no início do contêiner
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]