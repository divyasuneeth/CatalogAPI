import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(100), nullable=False)
    picture = Column(String(250))





class Category(Base):
    __tablename__='category'

    id=Column(Integer,primary_key=True)
    name=Column(String(250),nullable=False)

    @property
    def serialize(self):
        return {
           'id'     : self.id,
           'name'   :self.name,
       }


class ListItems(Base):
    __tablename__='listitems'

    name=Column(String(80),nullable=False)
    id=Column(Integer,primary_key=True)
    description=Column(String(250))
    category_id=Column(Integer,ForeignKey('category.id'))
    category=relationship(Category,backref='listitems')

    @property
    def serialize(self):
        return{
        'name':self.name,
        'id':self.id,
        'description':self.description
        }
engine= create_engine('sqlite:///categoryItems.db')

Base.metadata.create_all(engine)
