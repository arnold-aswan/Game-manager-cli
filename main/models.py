
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Table, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer(), primary_key=True)
    title = Column(String())
    genre = Column(String())
    platform = Column(String())
    price = Column(String())
    available = Column(Boolean())
    
    
    def __init__(self, title, genre, platform, price, available=True):
      self.id = None
      self.title = title
      self.genre = genre
      self.platform = platform
      self.price = price
      self.available = available
      
    def __repr__(self):
        return f'(Title= {self.title}, ' + \
            f'Genre = {self.genre}, ' + \
            f'Platform = {self.platform}, ' + \
            f'Price = {self.price}, ' + \
            f'available = {self.available})'             

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    email = Column(String())
    
    
    def __init__(self, name, email):
        self.id = None
        self.name = name
        self.email = email
        
    def __repr__(self):
        return f'(name = {self.name}, '+ \
            f'email = {self.email})'      
        

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer(), primary_key=True)
    quantity = Column(Integer())
    customer_id = Column(Integer(), ForeignKey('customers.id'))
    game_id = Column(Integer(), ForeignKey('games.id'))
    total_price = Column(Integer())
    
    def __init__(self, quantity, customer_id, game_id):
        self.id = None
        self.quantity = quantity
        self.customer_id = customer_id,
        self.game_id = game_id
        
      
    
