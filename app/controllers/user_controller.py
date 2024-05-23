from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from flask_bcrypt import check_password_hash, generate_password_hash

from app.models.usuario_model import Usuario
from app.models.jogo_model import Jogo
from app.instance import app, db
from service.helpers.helpers import Formulario_cadastro, FormularioUsuario, recupera_perfil

'''Definindo a rota home do site'''
@app.route("/")
def index():
    try:
        lista_jogos = []
        lista = Jogo.query.order_by(Jogo.id)
        usuarios = Usuario.query.order_by(Usuario.nickname)
        for usuario in usuarios:
                if(session['usuario_logado'] == usuario.nickname):
                    perfil = recupera_perfil(usuario.nickname)
                    for jogo in lista:
                        if jogo.usuario == usuario.nickname:
                            lista_jogos.append(jogo)
        return render_template('lista.html', titulo='Jogos', jogos=lista_jogos, perfil=perfil)
    except:
        return redirect(url_for('login'))
    

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    form = FormularioUsuario()
    return render_template('login.html', titulo='Faça seu login', proxima=proxima, form=form)

'''Cirando a rota -autenticar- para realizar a autenticação de usuário pela rota -login-'''
@app.route('/autenticar', methods=['POST'])
def autenticar():
    form = FormularioUsuario(request.form)
    
    # Debugging: Verificar se os dados do formulário estão sendo recebidos
    print(f"Form Data: Nickname - {form.nickname.data}, Senha - {form.senha.data}")
    
    # Encontrar usuário pelo nickname fornecido no formulário
    usuario = Usuario.query.filter_by(nickname=form.nickname.data).first()
    
    if usuario:
        print(f"Found user - Nickname: {usuario.nickname}, Hashed password: {usuario.senha}")
    else:
        print("User not found")
    
    if usuario and check_password_hash(usuario.senha, form.senha.data):
        session['usuario_logado'] = form.nickname.data
        flash(f"{form.nickname.data} logado com sucesso!")
        proxima_pagina = request.form.get('proxima')
        
        if not proxima_pagina or proxima_pagina == 'None':
            return redirect(url_for('index'))
        return redirect(proxima_pagina)
    else:
        if not usuario:
            flash('Usuário não encontrado!')
        else:
            flash('Senha incorreta!')
        
    return redirect(url_for('login'))


    """
    form = FormularioUsuario(request.form)
    usuarios = Usuario.query.order_by(Usuario.nickname)
    usuario = Usuario.query.filter_by(nickname=form.nickname.data).first()
    print(form.login.data)
    print('teste1')
    #print(usuario.nickname)
    print(usuario.senha)
    print(form.senha.data)
    print('teste^^')
    senha = check_password_hash(usuario.senha, form.senha.data)
    for usuario in usuarios:
        if usuario and senha:
            session['usuario_logado'] = request.form['usuario']
            flash(session['usuario_logado'] + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            
            if(proxima_pagina == 'None'):
                return redirect(url_for('index'))
            return redirect(proxima_pagina)
    else:
        flash('Usuário não logado!')
        return redirect(url_for('login'))
    """

'''Cirando a rota -logout- para realizar o logout do usuario'''
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Usuário deslogado!')
    return redirect(url_for('novo'))
    
'''Cirando a rota -create_user- para trazer a pagina html'''
@app.route('/create_user')
def create_user():
    form = Formulario_cadastro()
    return render_template('cadastro.html', titulo='Faça o seu cadastro', form=form)

'''Cirando a rota -register- para realizar a criação do usuário pela rota -create_user-'''
@app.route('/register',  methods=['POST'])
def register():
    form = Formulario_cadastro()
    
    '''Validando o formulario'''
    nome = form.usuario.data
    nickname = form.nickname.data
    senha = form.senha.data
    confirma_senha = form.confirma_senha.data
    print(senha)
    print(confirma_senha)
    
    usuario = Usuario.query.filter_by(nickname=nickname).first()
    if(usuario):
        flash('O Usuario já existe!')
        return redirect(url_for('login'))
    
    if(senha == confirma_senha):
        senha = generate_password_hash(senha)
        novo_usuario = Usuario(nome=nome,nickname=nickname, senha=senha)
        db.session.add(novo_usuario)
        
        '''Armazenando as imagens dos jogos'''
        arquivo = request.files['arquivo']
        perfis_path = app.config['PERFIS_PATH']
        arquivo.save(f'{perfis_path}/{novo_usuario.nickname}.jpg')
        
        db.session.commit()
        return redirect(url_for('login'))
    else:
        flash('Senha incompativeis!')
        return redirect(url_for('create_user'))
    
@app.route('/perfis/<arquivo>')
def imagem_perfil(arquivo):
    return send_from_directory('perfis', arquivo)