from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from DataBase.database import Tarefa

tarefa_route = Blueprint('tarefa', __name__)

@tarefa_route.route('/')
def listar_tarefas():
    """Listar as Tarefas"""
    tarefas = Tarefa.select()
    
    return render_template('listar_tarefas.html', tarefas=tarefas)

@tarefa_route.route('/new')
def formulario_tarefa():

    return render_template('form_tarefa.html')
@tarefa_route.route('/', methods=['POST'])
def inserir_tarefa():
    """Pegar os dados da tarefa no formulario para o back-end"""
    data = request.json

    if data['data'] == "":
        data['data'] = "Sem Prazo"
    if data['nome'] and data['data']:
        nova_tarefa = Tarefa.create(Nome=data['nome'], Prazo=data['data'])
        nova_tarefa.save()
    
    return render_template('item_tarefa.html', tarefa=nova_tarefa)
    # return f"""
    #     <li id="form-tarefa">
    #     <input type="checkbox" name="tarefa" id="checkbox">
    #     <span>{ nova_tarefa.Nome }</span>
    #     <div class="Action-buttons">
    #         <label class="view-btn" for="modal-toggle" c-get="{url_for('tarefa.detalhe_tarefa', tarefa_id=nova_tarefa.id)}" c-target="#modal-content">👁️</label>
    #         <button class="edit-btn">✏️</button>
    #         <button class="remove-btn" c-delete="{url_for('tarefa.deletar_tarefa', tarefa_id=nova_tarefa.id)}" c-remove-closest="li">🗑️</button>
    #     </div>
    # </li>
    #     """

@tarefa_route.route('<int:tarefa_id>')
def detalhe_tarefa(tarefa_id):
    """Exibir a tarefa detalhada"""
    tarefa = Tarefa.get_by_id(tarefa_id)
    
    return render_template('detalhe_tarefa.html', tarefa=tarefa)

@tarefa_route.route('<int:tarefa_id>/edit')
def editar_tarefa(tarefa_id):
    """Editar tarefa"""
    tarefa = Tarefa.get_by_id(tarefa_id)

    return render_template('form_tarefa.html', tarefa=tarefa)

@tarefa_route.route('<int:tarefa_id>/update', methods=['PUT'])
def atualizar_tarefa(tarefa_id):
    """Faça as Atualizações de tarefa"""
    tarefa_editar = Tarefa.get_by_id(tarefa_id)

    tarefa = request.json
    
    tarefa_editar.Nome = tarefa['nome']
    tarefa_editar.Prazo = tarefa['data']
    tarefa_editar.save()

    return render_template('item_tarefa.html', tarefa=tarefa_editar)

@tarefa_route.route('<int:tarefa_id>/delete', methods=['DELETE'])
def deletar_tarefa(tarefa_id):
    """Deletar tarefa"""

    tarefa = Tarefa.get_by_id(tarefa_id)
    tarefa.delete_instance()
    return {'deletado': 'ok'}