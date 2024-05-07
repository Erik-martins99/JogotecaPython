import os
from app.instance import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators


class Formulario_jogo(FlaskForm):
    nome = StringField('nome do jogo', [validators.data_required(), validators.length(min=1, max=50)])
    categoria = StringField('categoria', [validators.data_required(), validators.length(min=1, max=40)])
    console = StringField('console', [validators.data_required(), validators.length(min=1, max=20)])
    salvar = SubmitField('Salvar')
    
class Formulario_cadastro(FlaskForm):
    usuario = StringField('nome do jogo', [validators.data_required(), validators.length(min=1, max=250)])
    nickname = StringField('categoria', [validators.data_required(), validators.length(min=1, max=25)])
    senha = StringField('console', [validators.data_required(), validators.length(min=1, max=100)])
    confirma_senha = StringField('console', [validators.data_required(), validators.length(min=1, max=100)])
    salvar = SubmitField('Salvar')

def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo
        
    return 'capaPadrao.jpg'

def recupera_perfil(nickname):
    for nome_arquivo in os.listdir(app.config['PERFIS_PATH']):
        if f'{nickname}' in nome_arquivo:
            return nome_arquivo
        
    caminho = app.config['UPLOAD_PATH']    
    return os.path.join(caminho, 'capaPadrao.jpg')

def deleta_imagem(id):
    imagem = recupera_imagem(id)
    caminho = app.config['UPLOAD_PATH']
    if imagem != 'capaPadrao.jpg':
        os.remove(os.path.join(caminho, imagem))