from datetime import datetime
from flask import Flask, current_app, render_template, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')

from gestor import GestorDB
gestor= GestorDB()

@app.route('/')
def inicio():    
	return render_template('inicio.html')	

@app.route('/nuevoUsuario', methods = ['GET','POST'])
def nuevoUsuario():       
    if request.method == 'POST':
        if not request.form['nombre'] or not request.form['email'] or not request.form['password']:
            resultado=  render_template('aviso.html', mensaje="Los datos ingresados no son correctos...")
        else:
            existe= gestor.getUsuarioPorCorreo(request.form['email'])
            if existe == None:
                gestor.crearUsuario(request.form['nombre'], request.form['email'], request.form['password'])                
                resultado= render_template('aviso.html', mensaje="El usuario se registró exitosamente")
            else:
                resultado= render_template('aviso.html', mensaje='El correo electrónico se ha registrado anteriormente')
    else:
        resultado= render_template('nuevoUsuario.html')
    return resultado
	
@app.route('/nuevoComentario', methods = ['GET','POST'])
def nuevoComentario():    
    if request.method == 'POST':
        if  not request.form['email'] or not request.form['password']:
            resultado= render_template('aviso.html', mensaje="Por favor ingrese los datos requeridos")
        else:            
            usuarioActual= gestor.getUsuarioPorCorreo(request.form['email'])
            if usuarioActual is None:
                resultado= render_template('aviso.html', mensaje="El correo no está registrado")
            else:
                verificacion= usuarioActual.verificaClave(request.form['password'])
                if (verificacion):                    
                    resultado= render_template('ingresarComentario.html', nomUsuario = usuarioActual.getNombre())
                    session['userId'] = usuarioActual.getId()
                else:
                    resultado= render_template('aviso.html', mensaje="La contraseña  es incorrecta")
    else: # Cuando entro por GET
        resultado= render_template('nuevoComentario.html')
    return resultado

@app.route('/ingresarComentario', methods = ['GET', 'POST'])
def ingresarComentario():        
    if request.method == 'POST':
        if not request.form['contenido']:
            resultado= render_template('error.html', error="Contenido no ingresado...")
        else:          
            gestor.crearComentario(request.form['contenido'], session['userId'] )
            session.pop('userId', None)    
            resultado= render_template('aviso.html', mensaje="Se ha registrado el comentario")            
    else:
        resultado= render_template('inicio.html') 
    return resultado

@app.route('/listarComentarios')
def listarComentarios():   
   comentarios = gestor.getTodosComentarios()
   if comentarios != []:
       resultado = render_template('listarComentario.html', comentarios = comentarios)       
   else:
       resultado = render_template('aviso.html', mensaje="No se han registrado comentarios")  
   return resultado

@app.route('/selecUsuario', methods = ['GET', 'POST'])
def selecUsuario():      
    usuarios = gestor.getTodosUsuarios()  
    if usuarios != []:
        resultado= render_template('selecUsuario.html', usuarios = usuarios)
    else: 
        resultado= render_template('aviso.html', mensaje="No hay usuarios registrados") 
    return resultado

@app.route('/listarComentarioUsuario', methods=['GET', 'POST'])
def listarComentarioUsuario():
    resultado= render_template('aviso.html', mensaje="No se pudo ejecutar la operación")      
    if request.method == 'POST' and request.form['usuarios']:
        usuario = gestor.getUsuarioPorId(request.form['usuarios'])
        
        if usuario.hizoComentario():            
            resultado= render_template('listarComentarioUsuario.html', usuarioSelec = usuario) 
        else:
            resultado= render_template('aviso.html',mensaje='El usuario no ha hecho comentarios')
    return resultado

if __name__ == '__main__':     
    with app.app_context():   
        gestor.crearDB()       
        app.run(debug = True)              
        
    