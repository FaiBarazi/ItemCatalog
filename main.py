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
@app.route('/genres', methods=['GET'])
def mainPage():
    genres = session.query(Genre).all()
    return render_template('mainPage.html', genres=genres)

@app.route('/<int:genre_id>/movies',methods=['GET'])
def moviePage(genre_id):
    genre = session.query(Genre).filter_by(id=genre_id).one()
    movies = session.query(Movie).filter_by(genre_id=genre.id).all()
    return render_template('genreMovies.html', movies=movies,genre_name=genre.name)


@app.route('/<int:movie_id>/description',methods=['GET'])
def movieDescription(movie_id):
    movie = session.query(Movie).filter_by(id=movie_id).one()
    return render_template('movieDescription.html', movie_name=movie.name, 
                            description=movie.description)


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
