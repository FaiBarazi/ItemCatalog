from flask import Flask, flash, redirect, render_template, \
     request, url_for
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
@app.route('/genres')
def mainPage():
    genres = session.query(Genre).all()

    return render_template('mainPage.html', genres=genres)

@app.route('/genres/movies')
def moviePage():
    return 'I am the movies page'


@app.route('/genres/movies/description',methods=['GET'])
def movieDescription():
    return 'I am the description'

@app.route('/genres/movies/add', methods=['GET','POST'])
def movieAdd():
    return 'I am a movie to add'

@app.route('/genres/movies/edit',methods=['GET','PUT'])
def movieEdit():
    return 'I am a movie to edit'

@app.route('/genres/movies/delete',methods=['GET','DELETE'])
def movieDelete():
    return 'I am a movie to delete'

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
