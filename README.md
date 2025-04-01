# API de Carteira Digital (Digital Wallet API)

Uma API RESTful para gerenciamento de carteiras digitais e transações financeiras, desenvolvida com Django e Django REST Framework.

## 🚀 Funcionalidades Implementadas

- ✅ Autenticação JWT
- ✅ Gestão de usuários (registro, login)
- ✅ Carteiras digitais com saldo
- ✅ Operações financeiras:
  - Depósitos
  - Saques
  - Transferências entre usuários
- ✅ Histórico de transações com filtros por data
- ✅ Documentação Swagger/OpenAPI
- ✅ Containerização com Docker

## 🛠️ Tecnologias Utilizadas

- **Framework**: Django 4.2, Django REST Framework
- **Banco de Dados**: PostgreSQL
- **Autenticação**: JWT (JSON Web Tokens)
- **Containerização**: Docker e Docker Compose
- **Documentação**: Swagger/OpenAPI

## 📁 Estrutura do Projeto
````
payment-api/
├── core/ # Módulo principal
│ ├── exceptions.py # Exceções customizadas
│ ├── middlewares.py # Middlewares globais
│ └── utils/ # Utilitários
├── users/ # Módulo de usuários
│ ├── models.py # Modelo de usuário
│ ├── serializers.py # Serializers
│ ├── views.py # Views de autenticação
│ └── urls.py # Rotas de usuário
├── wallets/ # Módulo de carteiras
│ ├── models.py # Modelo de carteira
│ ├── serializers.py # Serializers
│ ├── views.py # Views de carteira
│ └── urls.py # Rotas de carteira
└── transactions/ # Módulo de transações
├── models.py # Modelo de transações
├── serializers.py # Serializers
├── views.py # Views de transações
└── urls.py # Rotas de transações
````


## ⚙️ Requisitos

- Python 3.11+
- Docker e Docker Compose
- PostgreSQL

## 🚀 Como Executar

### Usando Docker (Recomendado)

1. Clone o repositório:
```bash
git clone <repository-url>
cd payment-api
```

2. Inicie os contêineres:
```bash
docker-compose up -d
```

3. Acesse a API em: http://localhost:8000

### Configuração Manual

1. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure o banco de dados PostgreSQL

4. Execute as migrações:
```bash
python manage.py migrate
```

5. Inicie o servidor:
```bash
python manage.py runserver
```

## 📝 Endpoints da API

### Autenticação

```bash
# Registro de usuário
POST /api/auth/register/
{
    "username": "usuario",
    "email": "usuario@exemplo.com",
    "password": "senha123",
    "password_confirm": "senha123",
    "first_name": "Nome",
    "last_name": "Sobrenome"
}

# Login
POST /api/auth/login/
{
    "email": "usuario@exemplo.com",
    "password": "senha123"
}
```

### Carteira

```bash
# Consultar saldo
GET /api/wallet/

# Realizar depósito
POST /api/wallet/deposit/
{
    "amount": 100.00
}

# Realizar saque
POST /api/transactions/withdraw/
{
    "amount": 50.00,
    "description": "Saque em dinheiro"
}
```

### Transações

```bash
# Transferir para outro usuário
POST /api/transactions/transfer/
{
    "recipient_email": "outro@exemplo.com",
    "amount": 30.00,
    "description": "Pagamento"
}

# Listar transações
GET /api/transactions/

# Filtrar transações por data
GET /api/transactions/?start_date=2024-04-01&end_date=2024-04-30
```

## 🔒 Autenticação

A API utiliza autenticação JWT. Para acessar endpoints protegidos:

1. Faça login para obter o token
2. Inclua o token no header das requisições:


## 📊 Banco de Dados

O projeto utiliza PostgreSQL como banco de dados principal:

- Suporte a transações ACID
- Operações atômicas para transferências
- Consistência em operações concorrentes
- Relacionamentos entre usuários, carteiras e transações

## 📚 Documentação

A documentação completa da API está disponível em:
- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`

## 🧪 Testes

Execute os testes automatizados:

```bash
python manage.py test
```

## 🔍 Monitoramento

Você pode monitorar as transações e operações através:
- Admin do Django: `/admin/`
- Logs do Docker: `docker-compose logs -f`
- pgAdmin ou DBeaver para visualização do banco de dados

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie sua branch de feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request
