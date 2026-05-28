from __main__ import app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__= 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    clave = db.Column(db.String(120), nullable=False)    
    comentario = db.relationship('Comentario', backref='usuario', cascade='delete-orphan')
        
    def verificaClave(self, password):
        return check_password_hash(self.clave, password)
    
    def hizoComentario(self):
        return len(self.comentario) > 0
    
    def getId(self):
        return self.id    
    def getNombre(self):
        return self.nombre
    def getCorreo(self):
        return self.correo
    def getComentario(self):
        return self.comentario
	
class Comentario(db.Model):
    __tablename__= "comentario"

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime)
    contenido = db.Column(db.Text)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))      
    
    def getFecha(self):
        return self.fecha.strftime("%Y-%m-%d %H:%M:%S")
    
    def getContenido(self):
        return self.contenido
    

