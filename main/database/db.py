
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///main/database/games-manager.db')
Session = sessionmaker(bind=engine)
session = Session()
