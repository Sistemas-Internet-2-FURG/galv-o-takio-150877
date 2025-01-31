from flask_sqlalchemy import SQLAlchemy

# Instancia a extensão SQLAlchemy para uso com o Flask
db = SQLAlchemy()

# Define o modelo da tabela "Turma" no banco de dados
class Turma(db.Model):
    # Coluna 'id', chave primária, usada para identificar cada turma
    id = db.Column(db.Integer, primary_key=True)
    # Coluna 'nome', string de no máximo 80 caracteres, não pode ser nula
    nome = db.Column(db.String(80), nullable=False)
    # Relacionamento um-para-muitos com a tabela 'Aluno'. 
    # 'backref' cria um atributo 'turma' na classe Aluno para acessar a turma de um aluno.
    # 'lazy=True' define a forma como os dados relacionados são carregados 
    alunos = db.relationship('Aluno', backref='turma', lazy=True)
 
# Define o modelo da tabela "Aluno" no banco de dados
class Aluno(db.Model):
    # Coluna 'id', chave primária, usada para identificar cada aluno
    id = db.Column(db.Integer, primary_key=True)
    # Coluna 'nome', string de no máximo 80 caracteres, não pode ser nula
    nome = db.Column(db.String(80), nullable=False)
    # Coluna 'turma_id', chave estrangeira referenciando o campo 'id' da tabela 'Turma'
    # Relaciona o aluno com a turma correspondente
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=False)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(80), unique=True, nullable=False)
    senha = db.Column(db.String(128), nullable=False)
