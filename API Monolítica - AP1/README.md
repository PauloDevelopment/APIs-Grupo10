# API de Gerenciamento Escolar

## Integrantes
| Nome                          | RA      |
|-------------------------------|---------|
| Paulo Henrique Pires Cordeiro | 2402602 |
| Gustavo Meirelles Festa       | 2403079 |
| Miguel Condello Liando        | 2403877 |

## Descrição
A API foi criada para facilitar o gerenciamento de dados escolares, permitindo o controle de professores, turmas e alunos, bem como suas relações. Cada entidade possui validações específicas e as operações seguem boas práticas de desenvolvimento.

## Tecnologias Utilizadas
- Python 3
- Flask
- Flask-SQLAlchemy
- Flasgger (Swagger)
- SQLite
- Docker

## Como Executar

### Utilizando Docker
1. Certifique-se de ter o Docker instalado.
2. No diretório do projeto, construa a imagem:
   ```powershell
   docker build -t flask-api .
   ```
3. Rode o container:
   ```powershell
   docker run -p 5002:5002 flask-api
   ```
4. Acesse a documentação interativa em: [http://localhost:5002/apidocs](http://localhost:5002/apidocs)

### Utilizando Python diretamente
1. Instale as dependências:
   ```powershell
   pip install -r requirements.txt
   ```
2. Execute o servidor:
   ```powershell
   python app.py
   ```
3. Acesse a documentação interativa em: [http://localhost:5002/apidocs](http://localhost:5002/apidocs)

## Estrutura das Entidades
- **Professor**: id, nome, idade, matéria, observações
- **Turma**: id, descrição, ativo, professor_id
- **Aluno**: id, nome, idade, turma_id, data_nascimento, nota_primeiro_semestre, nota_segundo_semestre, media_final

## Endpoints Principais
- `/professores/` - CRUD de professores
- `/turmas/` - CRUD de turmas
- `/alunos/` - CRUD de alunos

## Documentação Swagger
A API conta com documentação automática via Swagger, detalhando todos os endpoints, parâmetros e exemplos de uso. Basta acessar `/apidocs` após iniciar o servidor.