# API de Carteira Digital

API RESTful para gerenciar carteiras digitais e transações financeiras, desenvolvida em Python com Django e Django REST Framework.

### Estrutura do Projeto
````
digital_wallet_api/
├── .env.example                     # Variáveis de ambiente de exemplo
├── .gitignore                       # Arquivos a serem ignorados pelo Git
├── Dockerfile                       # Configuração do Docker
├── docker-compose.yml               # Configuração do Docker Compose
├── requirements.txt                 # Dependências Python
├── manage.py                        # Script de gerenciamento Django
├── setup.py                         # Script de instalação
├── README.md                        # Documentação principal
├── CHANGELOG.md                     # Registro de alterações
├── LICENSE                          # Licença do projeto
├── digital_wallet/                  # Projeto Django principal
│   ├── __init__.py
│   ├── settings/                    # Configurações divididas por ambiente
│   │   ├── __init__.py
│   │   ├── base.py                  # Configurações base
│   │   ├── development.py           # Configurações de desenvolvimento
│   │   ├── production.py            # Configurações de produção
│   │   └── test.py                  # Configurações de teste
│   ├── urls.py                      # Roteamento principal de URLs
│   ├── asgi.py                      # Configuração ASGI
│   └── wsgi.py                      # Configuração WSGI
├── core/                            # Módulo principal com componentes compartilhados
│   ├── __init__.py
│   ├── exceptions.py                # Exceções customizadas
│   ├── middlewares.py               # Middlewares globais
│   └── utils.py                     # Funções utilitárias
├── users/                           # Módulo de usuários e autenticação
│   ├── __init__.py
│   ├── apps.py                      # Configuração do app
│   ├── urls.py                      # Rotas de autenticação
│   ├── models.py                    # Modelos de dados
│   ├── serializers.py               # Serializers para API
│   ├── services.py                  # Lógica de negócios
│   ├── repositories.py              # Acesso a dados
│   ├── permissions.py               # Permissões customizadas
│   └── views.py                     # Controllers/Views
├── wallets/                         # Módulo de carteiras digitais
│   ├── __init__.py
│   ├── apps.py                      # Configuração do app
│   ├── urls.py                      # Rotas da API de carteiras
│   ├── models.py                    # Modelos de dados
│   ├── serializers.py               # Serializers para API
│   ├── services.py                  # Lógica de negócios
│   ├── repositories.py              # Acesso a dados
│   └── views.py                     # Controllers/Views
├── transactions/                    # Módulo de transações
│   ├── __init__.py
│   ├── apps.py                      # Configuração do app
│   ├── urls.py                      # Rotas da API de transações
│   ├── models.py                    # Modelos de dados
│   ├── serializers.py               # Serializers para API
│   ├── services.py                  # Lógica de negócios
│   ├── repositories.py              # Acesso a dados
│   └── views.py                     # Controllers/Views
├── tests/                           # Testes automatizados
│   ├── __init__.py
│   ├── test_users.py                # Testes do módulo de usuários
│   ├── test_wallets.py              # Testes do módulo de carteiras
│   └── test_transactions.py         # Testes do módulo de transações
└── scripts/                         # Scripts utilitários
    ├── __init__.py
    ├── seed_db.py                   # Script para popular o banco
    └── generate_docs.py             # Script para gerar documentação
````

## 📋 Funcionalidades

- Autenticação com JWT
- Gestão de usuários
- Carteiras digitais
- Consulta de saldo
- Depósitos
- Transferências entre usuários
- Histórico de transações com filtros por data

## 🏗️ Arquitetura

O projeto segue uma arquitetura em camadas inspirada no Clean Architecture, com:

- **API Layer**: Controladores e serializers para interface HTTP
- **Service Layer**: Lógica de negócios
- **Repository Layer**: Acesso a dados
- **Security Layer**: Autenticação e autorização
- **Database Layer**: Persistência em PostgreSQL

Para mais detalhes, consulte a [documentação de arquitetura](docs/ARCHITECTURE.md).

## 🛠️ Tecnologias

- **Back-End**: Python 3.11, Django 4.2, Django REST Framework
- **Autenticação**: JWT (JSON Web Tokens)
- **Banco de Dados**: PostgreSQL
- **Contêinerização**: Docker, Docker Compose
- **Testes**: Pytest
- **Linter**: Flake8, Black
- **Documentação**: Swagger/OpenAPI

## 🚀 Instalação e Execução

### Pré-requisitos

- Python 3.11+
- PostgreSQL
- Docker e Docker Compose (opcional)

### Configuração com Docker (Recomendado)

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/digital-wallet-api.git
   cd digital-wallet-api
   ```

2. Crie o arquivo de variáveis de ambiente:
   ```bash
   cp .env.example .env
   ```

3. Inicie os contêineres:
   ```bash
   docker-compose up -d
   ```

4. Acesse a API em http://localhost:8000

### Configuração Manual

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/digital-wallet-api.git
   cd digital-wallet-api
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Crie o arquivo de variáveis de ambiente:
   ```bash
   cp .env.example .env
   ```
   
5. Edite o arquivo `.env` com suas configurações

6. Execute as migrações:
   ```bash
   python manage.py migrate
   ```

7. Popule o banco de dados com dados iniciais:
   ```bash
   python manage.py seed_db
   ```

8. Inicie o servidor:
   ```bash
   python manage.py runserver
   ```

9. Acesse a API em http://localhost:8000

## 📝 Uso da API

### Documentação da API

A documentação completa da API está disponível em:
- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`

### Autenticação

A API utiliza autenticação JWT (JSON Web Token). Para acessar endpoints protegidos:

1. Obtenha um token através do endpoint `/api/auth/login/`
2. Inclua o token no cabeçalho de suas requisições:
   ```
   Authorization: Bearer {seu_token_aqui}
   ```

### Exemplos de Requisições

#### Criar um usuário
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario",
    "email": "usuario@exemplo.com",
    "password": "senha123",
    "password_confirm": "senha123",
    "first_name": "Nome",
    "last_name": "Sobrenome"
  }'
```

#### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario",
    "password": "senha123"
  }'
```

#### Consultar saldo
```bash
curl -X GET http://localhost:8000/api/wallet/balance/ \
  -H "Authorization: Bearer {seu_token_aqui}"
```

#### Realizar depósito
```bash
curl -X POST http://localhost:8000/api/wallet/deposit/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {seu_token_aqui}" \
  -d '{
    "amount": 100.00
  }'
```

#### Transferir para outro usuário
```bash
curl -X POST http://localhost:8000/api/transactions/transfer/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {seu_token_aqui}" \
  -d '{
    "recipient_username": "outro_usuario",
    "amount": 50.00,
    "description": "Pagamento"
  }'
```

#### Listar transações
```bash
curl -X GET http://localhost:8000/api/transactions/ \
  -H "Authorization: Bearer {seu_token_aqui}"
```

## 🧪 Testes

### Executando Testes

```bash
# Todos os testes
pytest

# Testes específicos
pytest tests/test_users.py
pytest tests/test_wallets.py
pytest tests/test_transactions.py

# Com cobertura
pytest --cov=.
```

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie sua branch de feature (`git checkout -b feature/amazing-feature`)
3. Faça commit das suas alterações (`git commit -m 'Add some amazing feature'`)
4. Envie para a branch (`git push origin feature/amazing-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## ✨ Considerações sobre o Projeto

### Justificativa para uso do Django

O Django foi escolhido como framework por oferecer:
- ORM robusto e maduro
- Excelente integração com PostgreSQL
- Facilidade na implementação de autenticação e autorização
- Ecossistema rico em bibliotecas e plugins
- Django REST Framework como solução completa para APIs RESTful

### Justificativa para uso do PostgreSQL

O PostgreSQL foi escolhido como banco de dados por oferecer:
- ACID compliant para garantir a integridade dos dados financeiros
- Excelente performance em operações de leitura e escrita
- Tipos de dados avançados, incluindo JSON e Arrays
- Suporte a transações e locks para operações concorrentes
- Excelente suporte para Django ORM