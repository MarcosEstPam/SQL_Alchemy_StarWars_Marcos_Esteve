import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

characters_movies = Table('characters_movies', Base.metadata,
    Column('character_id', Integer, ForeignKey('character.id'), primary_key=True),
    Column('movie_id', Integer, ForeignKey('movies.id'), primary_key=True)
)

class Character(Base):
    __tablename__ = 'character'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    homeworld_id = Column(Integer, ForeignKey("planets.id"))

    homeworld = relationship('Planet', back_populates='residents') 
    movies = relationship('Movie', secondary=characters_movies, back_populates='characters')  

class Planet(Base):
    __tablename__ = 'planets'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False) 
    description = Column(String, nullable=True)  
    
    
    # Relación con personajes (un planeta puede tener varios personajes)
    residents = relationship('Character', back_populates='homeworld')

class Movie(Base):
    __tablename__ = 'movies'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)  
    release_date = Column(DateTime, nullable=True)  
    
    # Relación muchos a muchos con personajes
    characters = relationship('Character', secondary=characters_movies, back_populates='movies')


# class Person(Base):
#     __tablename__ = 'person'
#     # Here we define columns for the table person
#     # Notice that each column is also a normal Python instance attribute.
#     id = Column(Integer, primary_key=True)
#     name = Column(String(250), nullable=False)

# class Address(Base):
#     __tablename__ = 'address'
#     # Here we define columns for the table address.
#     # Notice that each column is also a normal Python instance attribute.
#     id = Column(Integer, primary_key=True)
#     street_name = Column(String(250))
#     street_number = Column(String(250))
#     post_code = Column(String(250), nullable=False)
#     person_id = Column(Integer, ForeignKey('person.id'))
#     person = relationship(Person)

#     def to_dict(self):
#         return {}

## Draw from SQLAlchemy base
render_er(Base, 'diagram.png')
