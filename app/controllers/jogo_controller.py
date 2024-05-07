from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory
from app.models.jogo_model import Jogo
from app.models.usuario_model import Usuario
from app.instance import app, db
from service.helpers.helpers import recupera_imagem, recupera_perfil, deleta_imagem, Formulario_jogo, Formulario_cadastro
import time
import os


'''Cirando a rota -novo- para trazer a pagina html'''
@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('novo')))
    else:
        perfil = recupera_perfil(session['usuario_logado'])
        form = Formulario_jogo()
        return render_template('novo.html', titulo='Novo Jogo', perfil=perfil, form=form)


'''Cirando a rota -criar- para realizar o cadastro do jogo pela rota -novo-'''
@app.route('/criar', methods=['POST',])
def criar():
    
    '''Validando o formulario'''
    form = Formulario_jogo(request.form)
    if(form.validate_on_submit()):
        return redirect(url_for('novo'))
        
    '''Pegando os valores do formulario'''
    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data
    
    '''Verificando se o jogo já está presente na lista de jogos'''
    j = Jogo.query.filter_by(nome=nome, usuario=session['usuario_logado']).first()
    if(j):
        flash('Jogo Já existente!')
        return redirect(url_for('index'))
    
    '''Salvando o jogo'''
    novo_jogo = Jogo(nome=nome, categoria=categoria, console=console, usuario=session['usuario_logado'])
    db.session.add(novo_jogo)
    db.session.commit()
    
    '''Armazenando as imagens dos jogos'''
    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{novo_jogo.id}-{timestamp}.jpg')
    
    return redirect(url_for('index'))
    
    
    
'''Cirando a rota -editar- para trazer a pagina html'''
@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('editar')))
    else:
        perfil = recupera_perfil(session['usuario_logado'])
        jogo = Jogo.query.filter(Jogo.id == id).first()
        
        '''Pegando os valores do formulario'''
        form = Formulario_jogo()
        form.nome.data = jogo.nome
        form.categoria.data = jogo.categoria
        form.console.data = jogo.console
        
        capa_jogo = recupera_imagem(id)
        return render_template('editar.html', titulo='Editando jogo', jogo=jogo, capa_jogo=capa_jogo, perfil=perfil, form=form)
   
   
    
'''Cirando a rota -atualizar- para editar os jogos no banco de dados'''
@app.route('/atualizar', methods=['POST',])
def atualizar():
    jogo = Jogo.query.filter_by(id=int(request.form['id'])).first()
    jogo.nome = request.form['nome']
    jogo.categoria = request.form['categoria']
    jogo.console = request.form['console']
    jogo.usuario = session['usuario_logado']
    
    db.session.add(jogo)
    db.session.commit()
    
    '''Armazenando as imagens dos jogos'''
    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    deleta_imagem(jogo.id)
    arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')
    
    return redirect(url_for('index'))



@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))
    else:
        Jogo.query.filter_by(id=id).delete()
        db.session.commit()
        flash(f'Jogo deletado com sucesso!')
        return redirect(url_for('index'))
    
@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)