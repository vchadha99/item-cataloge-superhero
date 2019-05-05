import os
import sys
from sqlalchemy import Column, ForeignKey, Integer ,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()

class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)

class Hero(Base):

    __tablename__ = 'Hero'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    power = relationship('Power', cascade='all, delete-orphan')
    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
        }

class Power(Base):
    __tablename__ = 'Power'
    id = Column(Integer, primary_key=True)
    powers = Column(String(250))
    hero_id = Column(Integer, ForeignKey('Hero.id'))
    hero = relationship(Hero, single_parent=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    @property
    def serialize(self):
        return {
            'powers': self.powers,
	    'id': self.id
        }

        
engine = create_engine('sqlite:///superhero.db')
Base.metadata.create_all(engine)