from flask import (Flask,
                   flash,
                   redirect,
                   render_template,
                   request,
                   url_for,
                   jsonify)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Genre, Movie, User
# Imports for Varification and Authentication
from flask import session as login_session
import random
import string
import json
# Handle Authentication
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
from flask import make_response
import requests
from functools import wraps

app = Flask(__name__)
# Connect to database
engine = create_engine('sqlite:///movieGenre.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Login Route
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "ItemCatalog"

# Checking for login


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in login_session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

# User login/logout setup


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    req = h.request(url, 'GET')[1]
    req_json = req.decode('utf8').replace("'", '"')
    result = json.loads(req_json)
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # Create User if it doesn't Exist
    user_id = getUserId(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as {}".format(login_session['username']))
    print("done!")
    return output

# Creating a new user


def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserId(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# disconnect from google


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token={}'.format(
        login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# Jason Routing


@app.route('/genre/<int:genre_id>/movies/JSON')
def moviesListJSON(genre_id):
    genre = session.query(Genre).filter_by(id=genre_id).one()
    movies = session.query(Movie).filter_by(genre_id=genre_id).all()
    return jsonify(Items=[i.serialize for i in movies])


@app.route('/genre/<int:genre_id>/<int:movie_id>/JSON')
def movieJSON(genre_id, movie_id):
    movie = session.query(Movie).filter_by(id=movie_id).one()
    return jsonify(movie.serialize)

# Add route to the main page


@app.route('/', methods=['GET'])
@app.route('/genre', methods=['GET'])
def homePage():
    genres = session.query(Genre).all()
    return render_template('homePage.html', genres=genres)


@app.route('/genre/<int:genre_id>/movies', methods=['GET'])
def showMovies(genre_id):
    genre = session.query(Genre).filter_by(id=genre_id).one()
    movies = session.query(Movie).filter_by(genre_id=genre.id).all()
    return render_template('showMovies.html',
                           genre_id=genre_id, genre=genre, movies=movies)

# Add a new movie route


@app.route('/genre/<int:genre_id>/new', methods=['GET', 'POST'])
@login_required
def newMovie(genre_id):
    genre = session.query(Genre).filter_by(id=genre_id).one()
    if request.method == 'POST':
        newmovie = Movie(name=request.form['name'],
                         description=request.form['description'],
                         user_id=login_session['user_id'], genre_id=genre_id)
        session.add(newmovie)
        session.commit()
        return(redirect(url_for('showMovies', genre_id=genre_id)))
    else:
        return render_template('newMovie.html', genre_id=genre_id,
                               genre_name=genre.name)


@app.route('/genre/<int:genre_id>/<int:movie_id>/description',
           methods=['GET', 'POST'])
def movieDescription(genre_id, movie_id):
    movie = session.query(Movie).filter_by(id=movie_id).one()
    return render_template('movieDescription.html', genre_id=genre_id,
                           movie_id=movie_id, movie=movie)

# Edit Movie Route


@app.route('/genre/<int:genre_id>/<int:movie_id>/movie/edit',
           methods=['GET', 'POST'])
@login_required
def movieEdit(genre_id, movie_id):
    movie = session.query(Movie).filter_by(id=movie_id).one()
    genre = session.query(Genre).filter_by(id=genre_id).one()
    if movie.user_id != login_session['user_id']:
        return 'You have no authorization to edit this movie.'
    if request.method == 'POST':
        if request.form['name']:
            movie.name = request.form['name']
        if request.form['description']:
            movie.description = request.form['description']
        session.add(movie)
        session.commit()
        return redirect(url_for('showMovies', genre_id=genre_id))
    else:
        return render_template('editMovie.html', genre_id=genre_id,
                               movie_id=movie_id, m=movie)

# Delete Movie Route


@app.route('/genre/<int:genre_id>/<int:movie_id>/delete',
           methods=['GET', 'POST'])
@login_required
def movieDelete(genre_id, movie_id):
    movie = session.query(Movie).filter_by(id=movie_id).one()
    genre = session.query(Genre).filter_by(id=genre_id).one()
    if movie.user_id != login_session['user_id']:
        return 'You have no authorization to delete this movie.'
    if request.method == 'POST':
        session.delete(movie)
        session.commit()
        return redirect(url_for('showMovies', genre_id=genre_id))
    else:
        return render_template('deleteMovie.html', genre_id=genre_id,
                               movie_id=movie_id, movie=movie)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
