from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Turma, Aluno

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'  # Configura o URI para o banco de dados SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desativa o rastreamento de modificações do SQLAlchemy
app.secret_key = 'supersecretkey'  # Necessário para usar mensagens flash (sessões seguras)
db.init_app(app)  # Inicializa o banco de dados com a aplicação Flask

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')  # Renderiza a página inicial

# Instância para Turmas
@app.route('/turmas', methods=['GET', 'POST'])
def manage_turmas():
    if request.method == 'POST':
        nome_turma = request.form.get('nome_turma')
        if nome_turma:  # Verifica se o nome da turma não está vazio
            nova_turma = Turma(nome=nome_turma)  # Cria uma nova instância de Turma
            db.session.add(nova_turma)  # Adiciona a nova turma à sessão do banco de dados
            db.session.commit()  # Salva as mudanças no banco de dados
            #flash('Turma adicionada com sucesso!', 'success')  # Exibe uma mensagem de sucesso
        return redirect(url_for('manage_turmas'))  # Redireciona para a página de gerenciamento de turmas

    turmas = Turma.query.all()  # Obtém todas as turmas do banco de dados
    return render_template('create_turma.html', turmas=turmas)  # Renderiza a página de gerenciamento de turmas

# Rota para editar uma turma
@app.route('/turmas/edit/<int:id>', methods=['GET', 'POST'])
def edit_turma(id):
    turma = Turma.query.get_or_404(id)  # Obtém a turma pelo ID ou retorna 404 se não encontrar
    
    if request.method == 'POST':
        nome_turma = request.form.get('nome_turma')
        if nome_turma:  # Verifica se o nome da turma não está vazio
            turma.nome = nome_turma  # Atualiza o nome da turma
            db.session.commit()  # Salva as mudanças no banco de dados
            #flash('Turma atualizada com sucesso!', 'success')  # Exibe uma mensagem de sucesso
        return redirect(url_for('manage_turmas'))  # Redireciona para a página de gerenciamento de turmas
    
    return render_template('edit_turma.html', turma=turma)  # Renderiza a página de edição da turma

# Rota para excluir uma turma
@app.route('/turmas/delete/<int:id>', methods=['POST'])
def delete_turma(id):
    turma = Turma.query.get_or_404(id)  # Obtém a turma pelo ID ou retorna 404 se não encontrar
    
    # Verifica se a turma possui alunos associados
    if Aluno.query.filter_by(turma_id=id).count() > 0:
        flash('Não é possível excluir a turma porque ela possui alunos associados.', 'error')  # Mensagem de erro
        return redirect(url_for('edit_turma', id=turma.id))  # Redireciona de volta para a página de edição da turma
    else:
        db.session.delete(turma)  # Remove a turma da sessão do banco de dados
        db.session.commit()  # Salva as mudanças no banco de dados
        #flash('Turma excluída com sucesso!', 'success')  # Exibe uma mensagem de sucesso
        return redirect(url_for('manage_turmas'))  # Redireciona para a página de gerenciamento de turmas

# Instância para Alunos
@app.route('/alunos', methods=['GET', 'POST'])
def manage_alunos():
    if request.method == 'POST':
        nome_aluno = request.form.get('nome_aluno')
        turma_id = request.form.get('turma_id')
        if nome_aluno and turma_id:  # Verifica se o nome do aluno e o ID da turma não estão vazios
            novo_aluno = Aluno(nome=nome_aluno, turma_id=turma_id)  # Cria uma nova instância de Aluno
            db.session.add(novo_aluno)  # Adiciona o novo aluno à sessão do banco de dados
            db.session.commit()  # Salva as mudanças no banco de dados
            #flash('Aluno adicionado com sucesso!', 'success')  # Exibe uma mensagem de sucesso
        return redirect(url_for('manage_alunos'))  # Redireciona para a página de gerenciamento de alunos

    alunos = Aluno.query.all()  # Obtém todos os alunos do banco de dados
    turmas = Turma.query.all()  # Obtém todas as turmas do banco de dados
    return render_template('create_aluno.html', alunos=alunos, turmas=turmas)  # Renderiza a página de gerenciamento de alunos

# Rota para editar um aluno
@app.route('/alunos/edit/<int:id>', methods=['GET', 'POST'])
def edit_aluno(id):
    aluno = Aluno.query.get_or_404(id)  # Obtém o aluno pelo ID ou retorna 404 se não encontrar
    
    if request.method == 'POST':
        nome_aluno = request.form.get('nome_aluno')
        turma_id = request.form.get('turma_id')
        if nome_aluno and turma_id:  # Verifica se o nome do aluno e o ID da turma não estão vazios
            aluno.nome = nome_aluno  # Atualiza o nome do aluno
            aluno.turma_id = turma_id  # Atualiza o ID da turma associada ao aluno
            db.session.commit()  # Salva as mudanças no banco de dados
            #flash('Aluno atualizado com sucesso!', 'success')  # Exibe uma mensagem de sucesso
        return redirect(url_for('manage_alunos'))  # Redireciona para a página de gerenciamento de alunos
    
    turmas = Turma.query.all()  # Obtém todas as turmas do banco de dados
    return render_template('edit_aluno.html', aluno=aluno, turmas=turmas)  # Renderiza a página de edição do aluno

# Rota para excluir um aluno
@app.route('/alunos/delete/<int:id>', methods=['POST'])
def delete_aluno(id):
    aluno = Aluno.query.get_or_404(id)  # Obtém o aluno pelo ID ou retorna 404 se não encontrar
    db.session.delete(aluno)  # Remove o aluno da sessão do banco de dados
    db.session.commit()  # Salva as mudanças no banco de dados
    #flash('Aluno excluído com sucesso!', 'success')  # Exibe uma mensagem de sucesso
    return redirect(url_for('manage_alunos'))  # Redireciona para a página de gerenciamento de alunos

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados se não existirem
    app.run(debug=False)  # Executa o aplicativo Flask em modo de depuração
