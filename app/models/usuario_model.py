from app.instance import db

'''Classe de modelo da tabela Usuario no DB'''
class Usuario(db.Model):
    nickname = db.Column(db.String(25), primary_key=True)
    nome = db.Column(db.String(250), nullable=False)
    senha = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return '<Name %r>' % self.name