
# Tutorial de Graphql con Flask y Ariadne

Creación de API Graphql con Flask, Ariadne y MySQL.


## Tabla de contenidos

* [Información general](#información-general)
* [Instalación](#instalación)
* [Tecnologías](#tecnologías)


## Información general

El proyecto consiste en un API Graphql de consulta de autores y libros. Se establece una relación "one to many" entre las tablas `authors` y `books`, de forma
que, al consultar los autores, poder acceder a los libros que tiene y, al consultar el libro, poder acceder a los datos del autor.
Creamos un servidor graphql con Flask y Ariadne. Usamos flask-sqlalchemy para los modelos y flask-marshmallow para los esquemas. Los datos de guardan en MySQL.

# Instalación

- Renombra el fichero `.env.example` a `.env`, inserta los valores correspondientes a tu conexión de base de datos.
- Crea el entorno virtual de desarrollo con `python -m venv venv`.
- Instala las dependencia con `pip install -r requirements.txt`.
- Inicializa el servidor de desarrollo con `flask --app main run`.


## Tecnologías

* [Flask](https://flask.palletsprojects.com/en/2.2.x/)
* [Ariadne](https://ariadnegraphql.org/)
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/)
* [Flask-Marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/)

## Authors

- [AlegreCode](https://github.com/AlegreCode)


## License

[MIT](https://choosealicense.com/licenses/mit/)


