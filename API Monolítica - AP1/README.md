# 🧠 Sistema de Gerenciamento | Microsserviços em Flask | AP2

Este projeto implementa três microsserviços em Flask para gerenciar dados acadêmicos: professores, turmas, alunos, reservas de sala e atividades/notas. Cada serviço é independente e se comunica com os demais via HTTP de forma síncrona, seguindo o padrão de arquitetura de microsserviços.

## 👥 Integrantes do Grupo

- Paulo Henrique Pires Cordeiro - 2402602	 
- Gustavo Meirelles Festa - 2403079
- Miguel Condello Liando - 2403877

---

## 🏗️ Arquitetura do Sistema

O sistema é dividido em três microsserviços:

| Microsserviço   | Responsabilidade                                              | Dependências                     |
|-----------------|---------------------------------------------------------------|----------------------------------|
| **Gerenciamento** | Cadastro e gerenciamento de alunos, professores e turmas     | Nenhuma                          |
| **Reservas**      | Gerenciamento de reservas de sala vinculadas a turmas        | Requer ID da Turma               |
| **Atividades**    | Gerenciamento de atividades e notas vinculadas a professores e turmas | Requer ID do Professor e da Turma |

Cada microsserviço possui:

- Estrutura baseada no padrão **MVC (Model-View-Controller)**
- Banco de dados **SQLite** com **SQLAlchemy ORM**
- Rotas RESTful com verbos HTTP: `GET`, `POST`, `PUT`, `DELETE`
- Documentação interativa com **Swagger**
- Comunicação síncrona via **requests** entre serviços

---

## 🐳 Execução com Docker Compose

### Pré-requisitos

- Docker instalado
- Docker Compose instalado

### Passos para execução

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. Execute os microsserviços com Docker Compose:
   ```bash
   docker-compose up --build
   ```

3. Acesse os serviços:

| Serviço        | URL Swagger                |
|----------------|----------------------------|
| Gerenciamento  | http://localhost:5000/docs |
| Reservas       | http://localhost:5001/docs |
| Atividades     | http://localhost:5002/docs |

---

## 🔌 Integração entre Microsserviços

A comunicação entre os microsserviços é feita de forma **síncrona**, utilizando a biblioteca `requests`. Cada serviço consome os IDs gerados pelos outros para vincular suas entidades:

- O serviço de **Reservas** consome o ID da Turma do serviço de Gerenciamento.
- O serviço de **Atividades** consome os IDs de Professor e Turma do serviço de Gerenciamento.

---

## 📚 Descrição das APIs

### Gerenciamento

- `GET /alunos` — Lista alunos  
- `POST /alunos` — Cria aluno  
- `PUT /alunos/<id>` — Atualiza aluno  
- `DELETE /alunos/<id>` — Remove aluno  
- Similar para `professores` e `turmas`

### Reservas

- `GET /reservas` — Lista reservas  
- `POST /reservas` — Cria reserva (requer ID da Turma)  
- `PUT /reservas/<id>` — Atualiza reserva  
- `DELETE /reservas/<id>` — Remove reserva

### Atividades

- `GET /atividades` — Lista atividades  
- `POST /atividades` — Cria atividade (requer ID do Professor e da Turma)  
- `PUT /atividades/<id>` — Atualiza atividade  
- `DELETE /atividades/<id>` — Remove atividade

---
