"""
Testes automatizados do TaskFlow.

IMPORTANTE (por que o GitHub Actions não reconhecia os testes):
- O arquivo precisa se chamar 'test_*.py' ou '*_test.py' (padrão do pytest).
- Precisa estar dentro da pasta 'tests/' referenciada no workflow.
- É necessário um 'pytest.ini' ou 'conftest.py' na raiz para que o
  pytest encontre o módulo 'app.py' ao rodar a partir de outra pasta.

Este arquivo cobre:
- Criação de tarefas (validação de entrada)
- Listagem de tarefas
- Busca de tarefa por ID
- Atualização de tarefas (incluindo validação de status)
- Remoção de tarefas
- Filtro por status (funcionalidade adicionada na mudança de escopo)
"""

import pytest
from app import app, reset_tasks


@pytest.fixture
def client():
    """Cria um cliente de testes do Flask e reseta o estado antes de cada teste."""
    reset_tasks()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_page(client):
    """Verifica se a rota inicial responde corretamente."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json()["mensagem"] == "TaskFlow API está funcionando!"


def test_create_task_success(client):
    """Testa a criação de uma tarefa válida."""
    response = client.post("/tasks", json={"titulo": "Estudar Engenharia de Software"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["titulo"] == "Estudar Engenharia de Software"
    assert data["status"] == "A Fazer"


def test_create_task_without_title_fails(client):
    """Testa a validação de entrada: criar tarefa sem título deve falhar."""
    response = client.post("/tasks", json={"descricao": "Faltou o título"})
    assert response.status_code == 400
    assert "erro" in response.get_json()


def test_list_tasks(client):
    """Testa se a listagem retorna todas as tarefas criadas."""
    client.post("/tasks", json={"titulo": "Tarefa 1"})
    client.post("/tasks", json={"titulo": "Tarefa 2"})

    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.get_json()) == 2


def test_get_task_by_id(client):
    """Testa a busca de uma tarefa específica pelo ID."""
    created = client.post("/tasks", json={"titulo": "Tarefa Única"}).get_json()

    response = client.get(f"/tasks/{created['id']}")
    assert response.status_code == 200
    assert response.get_json()["titulo"] == "Tarefa Única"


def test_get_task_not_found(client):
    """Testa a busca de uma tarefa inexistente."""
    response = client.get("/tasks/999")
    assert response.status_code == 404


def test_update_task(client):
    """Testa a atualização de uma tarefa existente."""
    created = client.post("/tasks", json={"titulo": "Tarefa Antiga"}).get_json()

    response = client.put(
        f"/tasks/{created['id']}",
        json={"titulo": "Tarefa Atualizada", "status": "Em Progresso"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["titulo"] == "Tarefa Atualizada"
    assert data["status"] == "Em Progresso"


def test_update_task_invalid_status(client):
    """Testa a validação de status inválido na atualização."""
    created = client.post("/tasks", json={"titulo": "Tarefa X"}).get_json()

    response = client.put(f"/tasks/{created['id']}", json={"status": "Status Inexistente"})
    assert response.status_code == 400


def test_delete_task(client):
    """Testa a remoção de uma tarefa."""
    created = client.post("/tasks", json={"titulo": "Tarefa a Remover"}).get_json()

    response = client.delete(f"/tasks/{created['id']}")
    assert response.status_code == 200

    # Confirma que a tarefa não existe mais
    response = client.get(f"/tasks/{created['id']}")
    assert response.status_code == 404


def test_filter_tasks_by_status(client):
    """Testa a funcionalidade adicionada na simulação de mudança de escopo."""
    client.post("/tasks", json={"titulo": "Tarefa A", "status": "Concluído"})
    client.post("/tasks", json={"titulo": "Tarefa B", "status": "A Fazer"})

    response = client.get("/tasks/filter?status=Concluído")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["titulo"] == "Tarefa A"


def test_filter_tasks_invalid_status(client):
    """Testa a validação do filtro com status inválido."""
    response = client.get("/tasks/filter?status=Inexistente")
    assert response.status_code == 400
