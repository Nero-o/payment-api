import os
import django
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digital_wallet.settings')
django.setup()

from django.core.management import call_command

def initialize_project():
    print("Aplicando migrações...")
    call_command('makemigrations')
    call_command('migrate')
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    if not User.objects.filter(is_superuser=True).exists():
        print("Criando superusuário...")
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            first_name='Admin',
            last_name='User',
            is_verified=True
        )
        print("Superusuário criado com sucesso!")
    else:
        print("Superusuário já existe.")
    
    print("Inicialização concluída.")

if __name__ == "__main__":
    initialize_project() 