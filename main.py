from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Genre, Movie

app = Flask(__name__)
engine = create_engine('sqlite:///movieGenre.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Add route to the main page
@app.route('/')
def mainPage():
    return 'I am the main page'

@app.route('/genre/movies')
def moviePage():
    return 'I am the movies page'

@app.route('/genre/movies/description')
def movieDescription():
    return 'I am the description'

@app.route('/genre/movies/add')
def movieAdd():
    return 'I am a movie to add'

@app.route('/genre/movies/edit')
def movieEdit():
    return 'I am a movie to edit'

@app.route('/genre/movies/delete')
def movieDelete():
    return 'I am a movie to delete'

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

