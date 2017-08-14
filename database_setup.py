import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# Create movie Genre SQL Table
class Genre(Base):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

# Create movies SQL Table
class Movie(Base):
    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String(250), nullable=False)
    genre_id = Column(Integer, ForeignKey('genre.id'))

engine = create_engine('sqlite:///movieGenre.db')
Base.metadata.create_all(engine)

