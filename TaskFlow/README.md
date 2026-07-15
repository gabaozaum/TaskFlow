# TaskFlow — Sistema de Gerenciamento de Tarefas

## 1. Objetivo do Projeto

O **TaskFlow** é um sistema web básico de gerenciamento de tarefas, desenvolvido para a
**TechFlow Solutions** a pedido de um cliente fictício (uma startup de logística). O objetivo
é permitir que a equipe acompanhe o fluxo de trabalho em tempo real, priorize tarefas
críticas e monitore o desempenho, através de um CRUD (Create, Read, Update, Delete)
simples e funcional, construído com **Python** e **Flask**.

Este projeto foi desenvolvido como atividade prática da disciplina de Engenharia de
Software, aplicando conceitos de metodologias ágeis, versionamento com Git/GitHub,
automação de testes e gestão de mudanças de escopo.

## 2. Escopo Inicial

O escopo inicial do projeto contemplava:

- CRUD completo de tarefas (criar, listar, buscar, atualizar e remover);
- Cada tarefa possui título, descrição e status (`A Fazer`, `Em Progresso`, `Concluído`);
- Validação de entradas (ex.: impedir criação de tarefa sem título, impedir status inválido);
- Testes automatizados cobrindo as principais rotas da API;
- Pipeline de integração contínua (CI) via GitHub Actions.

## 3. Metodologia Ágil Utilizada

Foi adotado o **Kanban**, por ser uma metodologia simples e visual, adequada para um
projeto de escopo pequeno e com poucos integrantes. O quadro foi organizado na aba
**Projects** do GitHub com três colunas:

| To Do (A Fazer) | In Progress (Em Progresso) | Done (Concluído) |
|---|---|---|
| Cards representando as funcionalidades planejadas | Cards em desenvolvimento no momento | Cards já finalizados e testados |

Diferente do Scrum, o Kanban não exige sprints fixas, o que se encaixou melhor no
ritmo de desenvolvimento incremental utilizado neste projeto.

## 4. Estrutura do Repositório

```
TaskFlow/
├── .github/
│   └── workflows/
│       └── python-tests.yml   # Pipeline de CI (GitHub Actions)
├── tests/
│   └── test_app.py            # Testes automatizados (pytest)
├── app.py                     # Código principal da aplicação (Flask)
├── requirements.txt           # Dependências do projeto
├── pytest.ini                 # Configuração do pytest
└── README.md
```

## 5. Como Executar o Sistema

### Pré-requisitos
- Python 3.12+ instalado

### Passo a passo

```bash
# 1. Clonar o repositório
git clone https://github.com/gabaozaum/TaskFlow.git
cd TaskFlow

# 2. Criar e ativar um ambiente virtual (opcional, mas recomendado)
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Rodar a aplicação
python app.py
```

A aplicação ficará disponível em `http://127.0.0.1:5000/`.

### Endpoints disponíveis

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Verifica se a API está no ar |
| POST | `/tasks` | Cria uma nova tarefa |
| GET | `/tasks` | Lista todas as tarefas |
| GET | `/tasks/<id>` | Busca uma tarefa específica |
| PUT | `/tasks/<id>` | Atualiza uma tarefa existente |
| DELETE | `/tasks/<id>` | Remove uma tarefa |
| GET | `/tasks/filter?status=` | Filtra tarefas por status *(adicionado na mudança de escopo)* |

## 6. Testes Automatizados

Os testes foram escritos com **pytest**, utilizando o cliente de testes do próprio Flask
(`test_client`), o que permite simular requisições HTTP sem precisar subir um servidor real.
São cobertos: criação, listagem, busca, atualização (incluindo validações), remoção e o
filtro por status.

Para rodar os testes localmente:

```bash
pytest tests/ -v
```

## 7. Integração Contínua (CI) — GitHub Actions

O pipeline configurado em `.github/workflows/python-tests.yml` é executado
automaticamente a cada `push` ou `pull request` nas branches `main`/`master`, e realiza:

1. Checkout do repositório;
2. Configuração do ambiente Python 3.12;
3. Instalação das dependências (`requirements.txt`);
4. Execução de todos os testes automatizados com `pytest`.

Isso garante que nenhuma alteração seja mesclada ao projeto sem antes passar pela
validação automática dos testes, reduzindo o risco de regressões.

## 8. Gestão de Mudanças — Simulação de Alteração de Escopo

**Mudança realizada:** adição do endpoint `GET /tasks/filter?status=`.

**Justificativa:** durante o desenvolvimento, identificou-se que o cliente (startup de
logística) precisava visualizar rapidamente apenas as tarefas de um determinado status
(por exemplo, apenas as que estão "Em Progresso"), sem precisar filtrar manualmente a
lista completa retornada pela rota `GET /tasks`. Essa necessidade não estava prevista no
escopo original, mas foi incorporada por representar um ganho real de usabilidade para o
time de operações do cliente, com baixo custo de implementação.

**Como foi gerenciada:**
1. Criado um novo card na coluna **A Fazer** do quadro Kanban: *"Implementar filtro de tarefas por status"*;
2. O card foi movido para **Em Progresso** durante o desenvolvimento da funcionalidade;
3. Foram adicionados testes automatizados específicos (`test_filter_tasks_by_status` e
   `test_filter_tasks_invalid_status`);
4. Após a validação via pipeline de CI, o card foi movido para **Concluído**;
5. A mudança foi documentada nesta seção do README, garantindo rastreabilidade da
   decisão.

## 9. Reflexão sobre Testes Automatizados

Os testes automatizados garantem que cada rota da API se comporte como esperado,
inclusive em cenários de erro (dados inválidos, recursos inexistentes). Isso permite
detectar regressões rapidamente sempre que uma nova alteração é enviada ao repositório,
sendo essencial para a confiabilidade do sistema em um contexto de entregas contínuas.

## 10. Autor

Projeto desenvolvido como atividade da disciplina de Engenharia de Software.
