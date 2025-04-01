# Arquitetura da API de Carteira Digital

Este documento descreve a arquitetura da API de Carteira Digital, seus componentes, fluxos de dados e decisões de design.

## Visão Geral da Arquitetura

A aplicação segue uma arquitetura em camadas baseada nos princípios do Clean Architecture, proporcionando:
- Separação clara de responsabilidades
- Baixo acoplamento entre componentes
- Alta testabilidade
- Manutenibilidade e extensibilidade

## Camadas da Arquitetura

### 1. API Layer (Presentation Layer)

Responsável por receber requisições HTTP, validar dados de entrada e formatar respostas.

**Componentes:**
- **Views/Controllers**: Endpoints da API que recebem requisições
- **Serializers**: Conversão entre formatos JSON e objetos Python
- **Validators**: Validação dos dados de entrada
- **Middlewares**: Processamento global de requisições

**Tecnologias:**
- Django REST Framework
- SimpleJWT para autenticação

**Responsabilidades:**
- Roteamento de URLs
- Validação de dados de entrada
- Aplicação de permissões e autenticação
- Formatação de respostas
- Tratamento de erros HTTP

### 2. Service Layer (Business Logic Layer)

Implementa a lógica de negócios da aplicação, independente de frameworks e infraestrutura.

**Componentes:**
- **Services**: Classes que implementam operações de negócio
- **Validators**: Validação de regras de negócio
- **DTOs**: Objetos de transferência de dados entre camadas

**Responsabilidades:**
- Implementar regras de negócio
- Orquestrar operações complexas
- Garantir a integridade dos dados
- Controlar transações

### 3. Repository Layer (Data Access Layer)

Responsável pelo acesso aos dados persistentes, abstraindo as operações do banco de dados.

**Componentes:**
- **Repositories**: Classes que encapsulam operações CRUD
- **Models**: Representações dos dados do domínio
- **Query Builders**: Construção de consultas complexas

**Tecnologias:**
- Django ORM

**Responsabilidades:**
- Abstrair operações de acesso a dados
- Mapear entre objetos de domínio e modelos do ORM
- Executar consultas ao banco de dados
- Gerenciar transações no nível de persistência

### 4. Database Layer

Responsável pelo armazenamento persistente dos dados.

**Tecnologia:**
- PostgreSQL

**Responsabilidades:**
- Armazenar dados de forma persistente
- Garantir integridade referencial
- Executar consultas SQL
- Manter índices para performance

## Fluxo de Dados

Um fluxo típico através das camadas:

1. O cliente envia uma requisição HTTP para a API
2. A camada API valida o token JWT e os dados de entrada
3. A requisição é encaminhada para o respectivo service
4. O service aplica a lógica de negócios, utilizando repositories conforme necessário
5. Os repositories interagem com o banco de dados, executando operações CRUD
6. O resultado é propagado de volta pelo service para a camada API
7. A API formata a resposta e a envia ao cliente

## Padrões de Design Utilizados

### Pattern Repository
- **Propósito**: Abstrair detalhes do acesso a dados
- **Implementação**: Classes repositories para cada entidade

### Injeção de Dependência
- **Propósito**: Reduzir acoplamento entre componentes
- **Implementação**: Dependências injetadas através de construtores

### Service Layer
- **Propósito**: Encapsular lógica de negócios
- **Implementação**: Classes service para cada funcionalidade

### DTO (Data Transfer Objects)
- **Propósito**: Transferir dados entre camadas
- **Implementação**: Classes específicas para transferência de dados

## Modelos de Dados

### User
Representa um usuário do sistema.

**Atributos principais:**
- `id`: Identificador único UUID
- `username`: Nome de usuário único
- `email`: Email do usuário
- `password`: Senha criptografada
- `first_name`: Primeiro nome
- `last_name`: Sobrenome

### UserProfile
Informações adicionais sobre o usuário.

**Atributos principais:**
- `user_id`: Referência ao usuário
- `phone_number`: Número de telefone
- `date_of_birth`: Data de nascimento
- `address`: Endereço

### Wallet
Carteira digital de um usuário.

**Atributos principais:**
- `id`: Identificador único UUID
- `user_id`: Referência ao proprietário
- `balance`: Saldo atual
- `created_at`: Data de criação
- `updated_at`: Data da última atualização

### Transaction
Registro de uma transação financeira.

**Atributos principais:**
- `id`: Identificador único UUID
- `wallet_id`: Carteira de origem
- `recipient_wallet_id`: Carteira de destino (opcional)
- `transaction_type`: Tipo (deposit, withdrawal, transfer)
- `amount`: Valor
- `description`: Descrição
- `status`: Estado (pending, completed, failed)
- `created_at`: Data de criação
- `completed_at`: Data de conclusão

## Segurança

### Autenticação
- JWT (JSON Web Token) para autenticação stateless
- Tokens de acesso e de refresh
- Expiração configurável de tokens

### Autorização
- Permissões baseadas em usuários
- Validação de propriedade de recursos

### Proteção de Dados
- HTTPS para comunicação segura
- Senhas armazenadas com hash bcrypt
- Sanitização de inputs
- Validação de dados em múltiplas camadas

## Tratamento de Erros

- Tratamento centralizado de exceções
- Respostas de erro padronizadas
- Logs estruturados
- Monitoramento de erros

## Considerações de Escalabilidade

- Conexões de banco de dados pooling
- Caching quando apropriado
- Paginação de resultados
- Indexação adequada no banco de dados

## Decisões Técnicas

### Escolha do Framework
Django e Django REST Framework foram escolhidos por:
- Ecosystem maduro e bem suportado
- ORM poderoso
- Funcionalidades de segurança integradas
- Excelente documentação

### Escolha do Banco de Dados
PostgreSQL foi escolhido por:
- Confiabilidade e maturidade
- Suporte a transações ACID
- Excelente performance para operações financeiras
- Boa integração com Django

### Escolha da Arquitetura
A arquitetura em camadas foi escolhida por:
- Facilitar testes unitários
- Permitir evolução independente de componentes
- Separar claramente responsabilidades
- Melhorar a manutenibilidade a longo prazo