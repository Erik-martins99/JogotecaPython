from app.instance import db

'''Classe de modelo da tabela Jogo no DB'''
class Jogo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(250), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    console = db.Column(db.String(50), nullable=False)
    usuario = db.Column(db.String(25), db.ForeignKey('usuario.nickname'), nullable=False)
    
    def __repr__(self):
        return '<Name %r>' % self.name