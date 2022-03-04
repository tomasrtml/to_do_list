import functools #set de funciones que se puede utilizar cuando estamos construyendo aplicaciones
from flask import(
    Blueprint, flash, g, render_template, request, url_for, session, redirect
)
#Blueprint: nos permite crear blueprints que son configurables. Un blueprint es una agrupación de módulos que hacen sentido.
#flash: nos permite enviar mensajes de manera genérica a nuestras plantillas, en caso de que tengamos errores.
#g: variables que podemos utilizar
#render_template: para renderizar plantillas
#request: para recibir datos desde un formulario
#url_for: para crear url's
#session: para mantener una referencia del usuario que se encuentra interactuando con nuestra app
from werkzeug.security import check_password_hash, generate_password_hash
#check_password_hash: para comprobar si una contraseña existe
#generate_password_hash para encriptar las contraseñas
from todo.db import get_db #para interactuar con nuestra DB

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error = None
        c.execute(
            'select id from user where username = %s', (username, ) #le ponemos una coma pq es una tupla
        )
        if not username:
            error = 'Username es requerido'
        if not password:
            error = 'Password es requerido'
        elif c.fetchone() is not None: #con fetchone buscamos al usuario y si no es None, entonces ya existe.
            error = 'Usuario {} se encuentra registrado.'.format(username)
        
        if error is None: #en caso de que no haya errores, incluimos al usuario nuevo a la DB
            c.execute(
                'insert into user (username, password) values (%s, %s)',
                (username, generate_password_hash(password))
            )
            db.commit()
            
            return redirect(url_for('auth.login'))
        #en caso de error mandamos el mensaje de error al cliente
        flash(error) 
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, c = get_db() 
        error = None
        c.execute(
            'select * from user where username = %s', (username, ) #le ponemos una coma pq es una tupla
        )
        user = c.fetchone()

        if user is None:
            error = 'Usuario y/o contraseña inválida'
        elif not check_password_hash(user['password'], password):
            error = 'Usuario y/o contraseña inválida'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('todo.index'))
        
        flash(error)
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db, c = get_db()
        c.execute(
            'select * from user where id = %s', (user_id,)
        )
        g.user = c.fetchone()

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None: #si es none, elusuario no ha iniciado sesión así que o redirigimos a la página de login
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


