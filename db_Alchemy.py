from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('postgresql://artemdenisov:@localhost/artemdenisov')

Base = declarative_base()

class Play(Base):
    __tablename__ = 'plays'  # имя таблицы в базе данных

    id = Column(Integer, primary_key=True)
    name = Column(String)

Session = sessionmaker(bind=engine)
session = Session()

new_play = Play(name = "play from alchemy")

session.add(new_play)

session.commit()

plays = session.query(Play).all()
for play in plays:
    print(play.id, play.name)

session.close()