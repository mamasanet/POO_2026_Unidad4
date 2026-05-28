from datetime import datetime
from werkzeug.security import generate_password_hash
from models import db, Usuario, Comentario

class GestorDB:
    def crearDB(self):
        db.create_all()

    def crearUsuario(self, nom, email, password):
        nuevoUsuario = Usuario(nombre= nom, correo= email , clave=generate_password_hash(password))       
        if not nuevoUsuario.id:
            db.session.add(nuevoUsuario)
            db.session.commit() 

    def getUsuarioPorCorreo(self, email):        
        return Usuario.query.filter_by(correo=email).first()         

    def getUsuarioPorId(self, id):
        return Usuario.query.get(id)

    def getTodosUsuarios(self):
        return Usuario.query.all()  
    
    def getNombre(self, userid): 
        return self.getUsuarioPorId(userid).getNombre()
           
    def crearComentario(self, contenido, userID ):
        nuevoComentario= Comentario(fecha=datetime.now(), contenido=contenido, usuario_id=userID)    
        if not nuevoComentario.id:
            db.session.add(nuevoComentario)
            db.session.commit() 

    def getTodosComentarios(self):
        return Comentario.query.all()  
   

    
    