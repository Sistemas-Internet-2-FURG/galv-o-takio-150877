from flask import Flask, request, jsonify
from models import db, Turma, Aluno, Admin
from flask_cors import CORS 
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import os

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração da chave secreta
app.secret_key = os.getenv('SECRET_KEY', 'supersecretkey')

from flask_cors import CORS

# Configuração do CORS para permitir o frontend na porta 3001
CORS(app, resources={r"/*": {"origins": ["http://localhost:3001", "http://10.10.38.129:3001"]}})


db.init_app(app)

# Rota para criar um novo administrador
#=-=-=-=-=-=-=-=-====-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#apenas adm do sistema
@app.route('/admins', methods=['POST'])
def create_admin():
    data = request.get_json()
    usuario = data.get('usuario')
    senha = data.get('senha')

    if not usuario or not senha:
        return jsonify({'error': 'Usuário e senha são obrigatórios'}), 400

    if Admin.query.filter_by(usuario=usuario).first():
        return jsonify({'error': 'Usuário já existe'}), 400

    senha_hash = generate_password_hash(senha)
    novo_admin = Admin(usuario=usuario, senha=senha_hash)
    db.session.add(novo_admin)
    db.session.commit()

    return jsonify({'message': 'Admin criado com sucesso!', 'id': novo_admin.id}), 201

# Rota para excluir um administrador
@app.route('/admins/<int:id>', methods=['DELETE'])
def delete_admin(id):
    admin = Admin.query.get_or_404(id)
    db.session.delete(admin)
    db.session.commit()
    return jsonify({'message': f'Admin {id} excluído com sucesso!'}), 200


# Consulta todos os administradores
@app.route('/admins', methods=['GET'])
def list_admins():
    admins = Admin.query.all()
    admins_data = [{'id': admin.id, 'usuario': admin.usuario} for admin in admins]
    return jsonify(admins_data), 200


#=-=-=-=-=-=-=-=-====-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

# Rota para login de administrador
@app.route('/admins/login', methods=['POST'])  # Define a rota para a URL "/admins/login" e aceita apenas o método POST.
def login_admin():
    # Obtém os dados enviados na requisição no formato JSON.
    data = request.get_json()
    usuario = data.get('usuario')  # Extrai o campo "usuario" dos dados JSON.
    senha = data.get('senha')  # Extrai o campo "senha" dos dados JSON.

    # Verifica se os campos "usuario" e "senha" foram fornecidos.
    if not usuario or not senha:
        return jsonify({'error': 'Usuário e senha são obrigatórios'}), 400  # Retorna erro 400 (Bad Request) se algum dos campos estiver ausente.

    # Busca o administrador no banco de dados pelo nome de usuário.
    admin = Admin.query.filter_by(usuario=usuario).first()
    # Verifica se o administrador existe e se a senha fornecida é válida.
    if not admin or not check_password_hash(admin.senha, senha):
        return jsonify({'error': 'Usuário ou senha inválidos'}), 401  # Retorna erro 401 (Unauthorized) se as credenciais forem inválidas.

    # Gera um token de autenticação usando o ID do administrador e a chave secreta do aplicativo.
    token = jwt.encode({'id': admin.id}, app.secret_key, algorithm='HS256')
    # Retorna uma mensagem de sucesso junto com o token gerado.
    return jsonify({'message': 'Login realizado com sucesso!', 'token': token}), 200

# Criar Turmas
@app.route('/turmas', methods=['POST'])
def create_turma():
    data = request.get_json()
    nome_turma = data.get('nome')

    if not nome_turma:
        return jsonify({'error': 'Nome da turma é obrigatório'}), 400

    nova_turma = Turma(nome=nome_turma)
    db.session.add(nova_turma)
    db.session.commit()

    return jsonify({'message': 'Turma criada com sucesso!', 'id': nova_turma.id}), 201

#Editar uma turma
@app.route('/turmas/<int:id>', methods=['PUT'])
def edit_turma(id):
    turma = Turma.query.get(id)
    if not turma:
        return jsonify({'error': 'Turma não encontrada'}), 404

    data = request.get_json()
    nome_turma = data.get('nome')

    if nome_turma:
        turma.nome = nome_turma

    db.session.commit()
    return jsonify({'message': f'Turma com ID {id} atualizada com sucesso!'}), 200

# Excluir turma
@app.route('/turmas/<int:id>', methods=['DELETE'])
def delete_turma(id):
    turma = Turma.query.get(id)
    if not turma:
        return jsonify({'error': 'Turma não encontrada'}), 404

    # Verifica se há alunos associados à turma
    if turma.alunos:  # Assume que a relação é `Turma.alunos`
        return jsonify({'error': 'Turma não pode ser excluída, pois possui alunos associados'}), 400

    # Se não houver alunos, exclui a turma
    db.session.delete(turma)
    db.session.commit()
    return jsonify({'message': f'Turma com ID {id} excluída com sucesso!'}), 200

# Consultar turmas  mostra todas as turmas listadas
@app.route('/turmas', methods=['GET'])
def list_turmas():
    turmas = Turma.query.all()
    turmas_data = [
        {
            'id': turma.id,
            'nome': turma.nome,
            'alunos': [{'id': aluno.id, 'nome': aluno.nome} for aluno in turma.alunos]
        }
        for turma in turmas
    ]
    return jsonify(turmas_data), 200

#=-=-==-=-==-=-=-=-=-=metodos que buscam o id e o nome do aluno em uma turma especifica-=-=-=-=-=-=-=-=
@app.route('/turmas/<int:id>', methods=['GET'])
def get_turma(id):
    turma = Turma.query.get(id)
    if not turma:
        return jsonify({'error': 'Turma não encontrada'}), 404
    return jsonify({'id': turma.id, 'nome': turma.nome}), 200


@app.route('/turmas/<int:id>/alunos', methods=['GET'])
def get_alunos_by_turma(id):
    turma = Turma.query.get(id)
    if not turma:
        return jsonify({'error': 'Turma não encontrada'}), 404
    alunos = [{'id': aluno.id, 'nome': aluno.nome} for aluno in turma.alunos]
    return jsonify(alunos), 200
#=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-0-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=



@app.route('/alunos', methods=['POST'])
def create_aluno():
    data = request.get_json()
    nome = data.get('nome')
    turma_id = data.get('turma_id')

    if not nome or not turma_id:
        return jsonify({'error': 'Nome e turma_id são obrigatórios'}), 400

    turma = Turma.query.get(turma_id)
    if not turma:
        return jsonify({'error': 'Turma não encontrada'}), 404

    # Cria um novo aluno
    novo_aluno = Aluno(nome=nome, turma_id=turma_id)
    db.session.add(novo_aluno)
    db.session.commit()

    # Retorna os dados completos do aluno recém-criado
    return jsonify({
        'message': 'Aluno criado com sucesso!',
        'id': novo_aluno.id,
        'nome': novo_aluno.nome,
        'turma_id': novo_aluno.turma_id
    }), 201

# Editar aluno
@app.route('/alunos/<int:id>', methods=['PUT'])
def edit_aluno(id):
    data = request.get_json()
    aluno = Aluno.query.get(id)
    if not aluno:
        return jsonify({'error': 'Aluno não encontrado'}), 404

    nome = data.get('nome')
    turma_id = data.get('turma_id')

    if nome:
        aluno.nome = nome
    if turma_id:
        turma = Turma.query.get(turma_id)
        if not turma:
            return jsonify({'error': 'Turma não encontrada'}), 404
        aluno.turma_id = turma_id

    db.session.commit()
    return jsonify({'message': f'Aluno com ID {id} atualizado com sucesso!'}), 200

# Excluir aluno
@app.route('/alunos/<int:id>', methods=['DELETE'])
def delete_aluno(id):
    aluno = Aluno.query.get(id)
    if not aluno:
        return jsonify({'error': 'Aluno não encontrado'}), 404

    db.session.delete(aluno)
    db.session.commit()
    return jsonify({'message': f'Aluno com ID {id} excluído com sucesso!'}), 200

# Listar alunos
@app.route('/alunos', methods=['GET'])
def list_alunos():
    alunos = Aluno.query.all()
    alunos_data = [{'id': aluno.id, 'nome': aluno.nome, 'turma_id': aluno.turma_id} for aluno in alunos]
    return jsonify(alunos_data), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=3000)
