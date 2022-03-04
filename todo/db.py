import mysql.connector
import click #para ejecutar comandos en la terminal.
from flask import current_app, g
#current_app mantiene la aplicación que estamos ejecutando
#g es una variable en la cual almacenaremos el usuario
from flask.cli import with_appcontext
#nos servirá cuando estemos ejecutando el sript de base de datos, ya que necesitaremos 
#el contexto de nuestra app
#cuando ejecutamos los scripts con app_context, podemos acceder a variables que se encuentran en la configuración de nuestra app, como el host, el pw y el user de la db
from .schema import instructions #aqui estarán los scripts para crear la db

#función para obtener la db y el cursor dentro de la app
def get_db():
    if 'db' not in g: #si el atributo db no está dentro de g
        g.db = mysql.connector.connect(
            host=current_app.config['DATABASE_HOST'],
            user=current_app.config['DATABASE_USER'],
            password=current_app.config['DATABASE_PASSWORD'],
            database=current_app.config['DATABASE']
        )
        g.c = g.db.cursor(dictionary=True) #para acceder a las propiedades como un diccionario
    return g.db, g.c #cada vez que llamemos a get_db(), otendremos la base de datos y el cursor

#función para cerrar la conexión con la db cada vez que realicemos una petición.
def close_db(e=None):
    db = g.pop('db', None) #quitamos la propiedad de db a g
    #si db no está definido, significa que nunca iniciamos la conexión, por lo que no es necesario cerrarla.
    #por otro lado, en caso de que sí esté definido, la cerramos:
    if db is not None:
        db.close()

#debemos indicarle a Flask que tiene que ejecutar close_db() al terminar una petición, por lo que configuramos
#nuestra aplicación mediante la siguiente función

def init_db():
    db, c = get_db()
    for i in instructions:
        c.execute(i)
    db.commit

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Base de datos inicializada')

def init_app(app):
    app.teardown_appcontext(close_db)
    #de esta manera, cada vez que realicemos una petición al servidor de flask que estamos construyendo
    #cuando esta petición termine, se llamará a la función close_db() para cerrar la conexión a la base de datos
    #la app de Flask que hemos creado es pasada como argumento a init_app(). En ella, llamamos a
    #teardown_appcontext, que ejecuta la función que le pasamos cuando estemos terminando la ejecución de 
    #algún método que hemos llamado.
    app.cli.add_command(init_db_command)





