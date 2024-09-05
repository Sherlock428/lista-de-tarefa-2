from flask import Flask
from routes.home import home_route
from routes.tarefas import tarefa_route
#inicializando flask
app = Flask(__name__)

#rotas
app.register_blueprint(home_route)
app.register_blueprint(tarefa_route, url_prefix='/tarefas')
#executar o código
app.run(debug=True)