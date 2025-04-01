#!/bin/bash
set -e

echo "Esperando o PostgreSQL iniciar..."
until pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER
do
  sleep 1
done
echo "PostgreSQL está pronto!"

# Criando diretórios de migrações
mkdir -p users/migrations
mkdir -p wallets/migrations
mkdir -p transactions/migrations
touch users/migrations/__init__.py
touch wallets/migrations/__init__.py
touch transactions/migrations/__init__.py

# Criar migrações para cada app separadamente
echo "Criando migrações para users..."
python manage.py makemigrations users

echo "Criando migrações para wallets..."
python manage.py makemigrations wallets

echo "Criando migrações para transactions..."
python manage.py makemigrations transactions

# Aplicar migrações na ordem correta
echo "Aplicando migrações de users..."
python manage.py migrate users

echo "Aplicando migrações de wallets..."
python manage.py migrate wallets

echo "Aplicando migrações de transactions..."
python manage.py migrate transactions

echo "Aplicando outras migrações..."
python manage.py migrate

# Criar superusuário
if [ "$CREATE_SUPERUSER" = "True" ]; then
    echo "Criando superusuário..."
    python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(email='admin@example.com').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123');
    print('Superusuário criado com sucesso!')
else:
    print('Superusuário já existe.')
"
fi

# Povoar o banco de dados
if [ "$SEED_DB" = "True" ]; then
    echo "Populando o banco de dados..."
    python manage.py seed_db
fi

# Iniciar o servidor
echo "Iniciando o servidor Django..."
exec "$@"