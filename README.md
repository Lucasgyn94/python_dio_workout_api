# Workout API - Uma API RESTful para Gerenciamento de Atletas e Treinos
Esta API RESTful foi desenvolvida com FastAPI, um framework moderno e rápido para construção de APIs em Python.<\br>Ela permite o gerenciamento completo de atletas, categorias de treino e centros de treinamento, oferecendo funcionalidades como cadastro, consulta, edição e exclusão de dados.

## Recursos Principais
Gerenciamento de Atletas:
Cadastro de novos atletas com informações como nome, CPF, idade, peso, altura, sexo, categoria e centro de treinamento.
Consulta de atletas por ID, nome ou CPF, com suporte a paginação para resultados otimizados.
Edição de informações de atletas existentes.
Exclusão de atletas.
Gerenciamento de Categorias:
Cadastro de novas categorias de treino.
Consulta de categorias por ID ou listagem completa.
Gerenciamento de Centros de Treinamento:
Cadastro de novos centros de treinamento com nome, endereço e proprietário.
Consulta de centros de treinamento por ID ou listagem completa.

## Tecnologias Utilizadas
FastAPI: Framework web de alta performance para construção de APIs.
SQLAlchemy: ORM (Object-Relational Mapper) para interação com o banco de dados PostgreSQL.
Alembic: Ferramenta para gerenciamento de migrações de banco de dados.
Pydantic: Biblioteca para validação de dados e criação de schemas.
FastAPI Pagination: Biblioteca para adicionar paginação aos endpoints da API.
Docker: Para conteinerização da aplicação, facilitando a implantação em diferentes ambientes.

## Como Executar a API
### Pré-requisitos:
Python 3.11+
Docker
Docker Compose

### Clone o Repositório:
Bash<\br>
git clone https://github.com/seu-usuario/workout-api.git

### Crie e Ative o Ambiente Virtual:
Bash
python -m venv venv
source venv/bin/activate

### Instale as Dependências:
Bash
pip install -r requirements.txt

### Execute as Migrações do Banco de Dados:
Snippet de código
alembic upgrade head

### Inicie a API:
Bash
uvicorn workout_api.main:app --reload<\br>
A API estará disponível em http://localhost:8000/.

## Endpoints
A documentação completa da API, incluindo detalhes sobre os endpoints, parâmetros e exemplos de requisições, está disponível em:<\br>
Swagger UI: http://localhost:8000/docs<\br>
Redoc: http://localhost:8000/redoc

## Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.
