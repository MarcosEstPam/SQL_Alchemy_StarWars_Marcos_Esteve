import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

# Tabla  para la relación muchos a muchos entre personajes y películas
characters_movies = Table('characters_movies', Base.metadata,
    Column('character_id', Integer, ForeignKey('character.id'), primary_key=True),
    Column('movie_id', Integer, ForeignKey('movies.id'), primary_key=True)
)

# Tabla  para los favoritos de personajes
favorites_characters = Table('favorites_characters', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('character_id', Integer, ForeignKey('character.id'), primary_key=True)
)

# Tabla  para los favoritos de planetas
favorites_planets = Table('favorites_planets', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('planet_id', Integer, ForeignKey('planets.id'), primary_key=True)
)

# Clase para los usuarios del blog
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    
    # Relación de favoritos (personajes y planetas)
    favorite_characters = relationship('Character', secondary=favorites_characters, back_populates='favorited_by')
    favorite_planets = relationship('Planet', secondary=favorites_planets, back_populates='favorited_by')

# Clase para los personajes
class Character(Base):
    __tablename__ = 'character'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    homeworld_id = Column(Integer, ForeignKey("planets.id"))
    favorites = Column(String, nullable=False)

    homeworld = relationship('Planet', back_populates='residents') 
    movies = relationship('Movie', secondary=characters_movies, back_populates='characters')
    
    # Relación con usuarios que han guardado este personaje como favorito
    favorited_by = relationship('User', secondary=favorites_characters, back_populates='favorite_characters')

# Clase para los planetas
class Planet(Base):
    __tablename__ = 'planets'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    # Relación con personajes (un planeta puede tener varios personajes)
    residents = relationship('Character', back_populates='homeworld')
    
    # Relación con usuarios que han guardado este planeta como favorito
    favorited_by = relationship('User', secondary=favorites_planets, back_populates='favorite_planets')

# Clase para las películas
class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(DateTime, nullable=True)

    # Relación muchos a muchos con personajes
    characters = relationship('Character', secondary=characters_movies, back_populates='movies')

# Generar el diagrama ER
try:
    result = render_er(Base, 'diagram.png')
    print("Diagrama generado correctamente.")
except Exception as e:
    print("Error al generar el diagrama:", e)


