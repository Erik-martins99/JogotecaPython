import os

'''Configurando a chave secreta para implementação nos cookes do navegador'''
SECRET_KEY = 'alura'

'''Conectando ao banco de dados ?driver=SQL+Server ?trusted_connection=yes'''
SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://192.168.0.47\\DETRANBA/ambiente_teste?driver=SQL+Server&trusted_connection=yes'

#UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'

#PERFIS_PATH = os.path.dirname(os.path.abspath(__file__)) + '/perfis'

config_dir = os.getcwd()

UPLOAD_PATH = os.getcwd() + '//app/uploads'

PERFIS_PATH = os.getcwd() + '//app/perfis'
