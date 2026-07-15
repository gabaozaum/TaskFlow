"""
TaskFlow - Sistema de Gerenciamento de Tarefas
------------------------------------------------
Sistema web básico desenvolvido em Flask, implementando um CRUD
(Create, Read, Update, Delete) completo para gerenciamento de tarefas.

Este projeto simula o desenvolvimento de um sistema real para a
TechFlow Solutions, aplicando conceitos de Engenharia de Software,
metodologias ágeis e controle de qualidade via testes automatizados.
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

# ------------------------------------------------------------------
# "Banco de dados" em memória (lista de dicionários).
# Em um sistema real, isso seria substituído por um banco de dados
# (ex.: PostgreSQL, SQLite, MongoDB).
# ------------------------------------------------------------------
tasks = []
next_id = 1


def reset_tasks():
    """Reseta o estado da lista de tarefas (usado principalmente nos testes)."""
    global tasks, next_id
    tasks = []
    next_id = 1


@app.route("/")
def home():
    """Rota inicial - apenas confirma que a API está no ar."""
    return jsonify({"mensagem": "TaskFlow API está funcionando!"})


# ------------------------------------------------------------------
# CREATE - Criar uma nova tarefa
# ------------------------------------------------------------------
@app.route("/tasks", methods=["POST"])
def create_task():
    global next_id
    data = request.get_json(silent=True)

    # Validação de entrada: garante que o campo "titulo" foi enviado
    if not data or "titulo" not in data or not data["titulo"].strip():
        return jsonify({"erro": "O campo 'titulo' é obrigatório."}), 400

    task = {
        "id": next_id,
        "titulo": data["titulo"],
        "descricao": data.get("descricao", ""),
        "status": data.get("status", "A Fazer"),
    }
    tasks.append(task)
    next_id += 1

    return jsonify(task), 201


# ------------------------------------------------------------------
# READ - Listar todas as tarefas
# ------------------------------------------------------------------
@app.route("/tasks", methods=["GET"])
def list_tasks():
    return jsonify(tasks), 200


# ------------------------------------------------------------------
# READ - Buscar uma tarefa específica pelo ID
# ------------------------------------------------------------------
@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"erro": "Tarefa não encontrada."}), 404
    return jsonify(task), 200


# ------------------------------------------------------------------
# UPDATE - Atualizar uma tarefa existente
# ------------------------------------------------------------------
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"erro": "Tarefa não encontrada."}), 404

    data = request.get_json(silent=True) or {}

    # Validação: se o status for enviado, deve ser um dos valores permitidos
    status_validos = ["A Fazer", "Em Progresso", "Concluído"]
    if "status" in data and data["status"] not in status_validos:
        return jsonify({
            "erro": f"Status inválido. Use um dos seguintes: {status_validos}"
        }), 400

    task["titulo"] = data.get("titulo", task["titulo"])
    task["descricao"] = data.get("descricao", task["descricao"])
    task["status"] = data.get("status", task["status"])

    return jsonify(task), 200


# ------------------------------------------------------------------
# DELETE - Remover uma tarefa
# ------------------------------------------------------------------
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"erro": "Tarefa não encontrada."}), 404

    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"mensagem": "Tarefa removida com sucesso."}), 200


# ------------------------------------------------------------------
# FUNCIONALIDADE ADICIONAL (Simulação de Mudança de Escopo)
# Filtro de tarefas por status - adicionado após solicitação do
# cliente (ver justificativa no README.md, seção "Gestão de Mudanças").
# ------------------------------------------------------------------
@app.route("/tasks/filter", methods=["GET"])
def filter_tasks_by_status():
    status = request.args.get("status")
    status_validos = ["A Fazer", "Em Progresso", "Concluído"]

    if status is None:
        return jsonify({"erro": "Informe o parâmetro 'status' na URL."}), 400

    if status not in status_validos:
        return jsonify({
            "erro": f"Status inválido. Use um dos seguintes: {status_validos}"
        }), 400

    resultado = [t for t in tasks if t["status"] == status]
    return jsonify(resultado), 200


if __name__ == "__main__":
    app.run(debug=True)
