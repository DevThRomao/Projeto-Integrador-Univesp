from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from models import db, Voluntario

app = Flask(__name__)
app.secret_key = 'senha123'

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voluntarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Iniciar o SQLAlchemy com o app
db.init_app(app)


@app.route('/')
def index():
    return render_template ('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        endereço = request.form['endereço']
        # Salvar os dados em um novo registro de voluntário no banco de dados
        novo_voluntario = Voluntario(nome=nome, email=email, telefone=telefone, endereço=endereço)
        db.session.add(novo_voluntario)
        db.session.commit()
        return redirect(url_for('voluntarios'))
    return render_template('cadastro.html')

@app.route('/voluntarios')
def voluntarios():
    voluntarios = Voluntario.query.all()
    return render_template('voluntarios.html', voluntarios=voluntarios)

@app.route('/buscar_voluntarios', methods=['GET'])
def buscar_voluntarios():
    termo_busca = request.args.get('termo_busca', '')
    voluntarios = Voluntario.query.filter(
        (Voluntario.nome.ilike(f'%{termo_busca}%')) |
        (Voluntario.email.ilike(f'%{termo_busca}%')) |
        (Voluntario.endereço.ilike(f'%{termo_busca}%'))

    ).all()
    return render_template('voluntarios.html', voluntarios=voluntarios)

@app.route('/admvoluntarios')
def administrar_voluntarios():
    voluntarios = Voluntario.query.all()
    return render_template('admvoluntarios.html', voluntarios=voluntarios)
@app.route('/editar_voluntario/<int:id>', methods=['GET', 'POST'])
def editar_voluntario(id):
    voluntario = Voluntario.query.get_or_404(id)
    if request.method == 'POST':
        # Atualize os dados do voluntário com base no formulário enviado
        voluntario.nome = request.form['nome']
        voluntario.email = request.form['email']
        voluntario.telefone = request.form['telefone']
        voluntario.endereço = request.form['endereço']
        db.session.commit()
        return redirect(url_for('administrar_voluntarios'))
    return render_template('editar_voluntario.html', voluntario=voluntario)

@app.route('/excluir_voluntario/<int:id>')
def excluir_voluntario(id):
    voluntario = Voluntario.query.get_or_404(id)
    db.session.delete(voluntario)
    db.session.commit()
    return redirect(url_for('administrar_voluntarios'))


if __name__ == '__main__':
    # Usar app.app_context() para criar o banco de dados
    with app.app_context():
        db.create_all()
    app.run(debug=True)











