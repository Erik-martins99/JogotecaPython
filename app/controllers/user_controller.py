from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from app.models.usuario_model import Usuario
from app.models.jogo_model import Jogo
from app.instance import app, db
from service.helpers.helpers import Formulario_cadastro, recupera_perfil

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
    return render_template('login.html', titulo='Faça seu login', proxima=proxima)

'''Cirando a rota -autenticar- para realizar a autenticação de usuário pela rota -login-'''
@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuarios = Usuario.query.order_by(Usuario.nickname)
    for usuario in usuarios:
        if(request.form['usuario'] == usuario.nickname and request.form['senha'] == usuario.senha):
            session['usuario_logado'] = request.form['usuario']
            flash(session['usuario_logado'] + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            print(proxima_pagina)
            if(proxima_pagina == 'None'):
                return redirect(url_for('index'))
            return redirect(proxima_pagina)
    else:
        flash('Usuário não logado!')
        return redirect(url_for('login'))

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
    
    usuario = Usuario.query.filter_by(nickname=nickname).first()
    if(usuario):
        flash('O Usuario já existe!')
        return redirect(url_for('login'))
    
    if(senha == confirma_senha):
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