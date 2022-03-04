import os #lo usaremos para acceder a las variables de entorno
from flask import Flask

#Cuando separamos todo en distintos módulos, usamos una función que llamaremos
#create_app, la que nos servirá más adelante para hacer testing o para crear varias
#instancias de la aplicación (por ahora crearemos solo una).
def create_app():
    #definimos la constante app mediante el constructor de Flask
    app = Flask(__name__)
    #utilizamos las variables de entorno para configurar nuestra aplicación
    #from_mapping nos permite definir variables de configuración que dps podremos utilizar en nuestra app.
    app.config.from_mapping(
        SECRET_KEY='mikey',
        #utilizada para definir las sesiones en nuestra app. Una sesión es cuando generamos una llave 
        # que será enviada al usuario para ser usada como referencia con datos guardados en el servidor
        #(lo que le enviamos es una cookie que tendrá un identificador único, y así podremos saber qué tipos de datos están asociados al usuario).
        #por ahora le ponemos un string simple 'mikey', pero en producción se ponen strongs más complicados
        #para evitar que los hackers identifiquen cómo estamos generando nuestras sesiones.
        DATABASE_HOST='localhost', #os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_PASSWORD='#revoLver66',#os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER='tomasql',#os.environ.get('FLASK_DATABASE_USER'),
        DATABASE='prueba'#os.environ.get('FLASK_DATABASE')
        #DB a la que nos queremos conectar
        #environ 'es el objeto que contiene todas las variables de entorno'
    )
    from . import db

    db.init_app(app)

    from . import auth
    from . import todo

    app.register_blueprint(auth.bp)
    app.register_blueprint(todo.bp)
    
    @app.route('/hola')
    def hola():
        return "paja"
    
    return app