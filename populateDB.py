from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Genre, Base, Movie

engine = create_engine('sqlite:///movieGenre.db')
Base.metadata.bind = engine
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
DBSession = sessionmaker(bind=engine)

session = DBSession()

#Horror movies
horror = Genre(name='Horror')
session.add(horror)
session.commit()

movieItem1 = Movie(name='Get Out', description='''Meet the parents  movie that turns into horror when the son-in-low comes to visit. The moral, never trutst your parents in law''', genre=horror)
session.add(movieItem1)
session.commit()

movieItem2 = Movie(name='Raw', description='''The life of a stringent vegetarian Justine turns upside down when she attends a veterinary school, can she keep up with her diet? ''', genre=horror)
session.add(movieItem2)
session.commit()

#Romance Movies
romance = Genre(name='Romance')
session.add(romance)
session.commit()

movieItem1 = Movie(name='The Big Sick',description='''The film tells the story of Pakistan-born aspiring comedian who connects with grad student after one of his standup sets.However, what they thought would be just a one-night stand blossoms into the real thing, which complicates things epsicially with his traditional Muslim parents''',
                   genre=romance)
session.add(movieItem1)
session.commit()

movieItem2 = Movie(name='Paris Pieds Nus',description='''Fiona, a Canadian librarian leaves to Paris to help her aging grand mother. However, she loses her way and her grand mother gets lost. The search begins in Paris with her new-friend Dom, a homeless man in Paris who is attracted to Fiona.''', 
                   genre=romance)
session.add(movieItem2)
session.commit()

scifi = Genre(name='Sci Fi')
session.add(scifi)
session.commit()

animated = Genre(name='Animated')
session.add(animated)
session.commit()

