
------

# Agente Autônomo para Sugestão de Melhorias de Código

## 1. Project Overview

**What is your project about?**  
This project consists in an API that has 2 main endpoints: <br>
/code_analyzer -> which connects with GeminiAI in order to fetch improvement recommendations for a given python code
/crewai_code_analyzer -> which uses crewai in order to do 3 things: 1. fetch recommendations; 2. implement a code with found suggestions; 3. generate a report with everything that was done 

**What problem does it solve or what goal does it achieve?**  
It analyzes source code and provides recommendations for improvement based on best programming practices.

---

## 2. Features

### Key Features:
- **/health**: Endpoint to check the agent's status.
- **/analyze-code**: Endpoint to submit source code and receive improvement suggestions.
- **/crewai_code_analyzer**: Endpoint to submit source code and start crewai agents.
- **/analysis**: Endpoint to retrieve all the analyses performed, which are stored in a PostgreSQL database.

### APIs & Integrations:
- Integration with **Gemini AI** for generating code improvement suggestions.

---

## 3. Installation

### Steps to Install the Project Locally:
1. Install the dependencies with:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the FastAPI server with:
   ```bash
    fastapi dev main.py
   ```
Use tools like Insomnia or Postman to consume the API endpoints.

### Dependencies and prerequisites
Check requirements.txt

## 4. Usage

Here’s an example of how to use the **/analysis** endpoint with a **POST** request:

```bash
curl --request POST \
  --url http://localhost:8000/crewai_code_analyzer \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/9.2.0' \
  --data '{
    "code": "print('\''Hello World'\'')"
}'
```

## 5. Configuration

### Environment Variables:
Adicione as seguintes variáveis no arquivo `.env`:

```dotenv
GEMINI_API_KEY="sua-chave-api-do-gemini-aqui"
DB_USER=<your-username>
DB_PASSWORD=<your-password>
DB_HOST=localhost
DB_PORT=5432
DB_NAME=analysis
```
### Database Setup:

1. Instale o **PostgreSQL** a partir de [aqui](https://www.postgresql.org/download/).

2. Após a instalação, abra o terminal e execute os seguintes comandos:

   ```bash
   psql -U $(whoami)  # Isso utiliza o nome de usuário padrão do sistema
   postgres=# CREATE USER analyzer WITH PASSWORD 'pass2025mirante';
   postgres=# CREATE DATABASE analysis;
   postgres=# GRANT ALL PRIVILEGES ON DATABASE analysis TO analyzer;
   ```
3. Após configurar o banco de dados, o projeto estará pronto para armazenar as análises.

## 6. Technologies Used

- **FastAPI**: Framework para criação de APIs rápidas e eficientes em Python.
- **SQLAlchemy**: ORM (Object Relational Mapper) utilizado para interagir com o banco de dados PostgreSQL.
- **GeminiAI**: API de inteligência artificial utilizada para fornecer sugestões de melhoria de código.
- **CrewAI**: Plataforma de múltiplos agents utilizada para criar agents que executam tasks para atingir o objetivo do projeto.
- 
## 7. Project Structure

A estrutura do projeto é a seguinte:
```bash
/controller
  ├── analyze_code.py
  ├── crewai_analyze_code.py

/db_connection.py
/models.py
main.py
```
- **/controller/analyze_code.py**: Contém a lógica para lidar com as requisições de análise de código.
- **/controller/crewai_analyze_code.py**: Contém a lógica para criar uma crew, agents e tasks.
- **/db_connection.py**: Gerencia a conexão com o banco de dados PostgreSQL.
- **/models.py**: Define os modelos de dados e o esquema para os resultados das análises.
- **main.py**: Inicia o servidor FastAPI e expõe os endpoints da API.




 
