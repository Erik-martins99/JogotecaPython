from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config.config import config_dir



class Server:
    
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config.from_pyfile(f'{config_dir}\config\config.py')
        
        self.db = SQLAlchemy(self.app)
        
    def run(self):
        self.app.run(debug=True)
        
server = Server()
db = server.db
app = server.app