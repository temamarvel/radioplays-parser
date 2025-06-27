import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

connection_string = f"postgresql://{DB_USER}:@{DB_HOST}/{DB_NAME}"

engine = create_engine(connection_string)

Base = declarative_base()
# todo make method to create a record in DB
class Play(Base):
    __tablename__ = "plays"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    s3_key = Column(String, nullable=False)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

new_play = Play(name = "play from alchemy", s3_key = "key")

session.add(new_play)

session.commit()

plays = session.query(Play).all()
for play in plays:
    print(play.id, play.name, play.s3_key)

session.close()