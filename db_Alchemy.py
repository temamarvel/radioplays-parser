import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from colored import Fore, Back, Style

from db_models import Play

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

connection_string = f"postgresql://{DB_USER}:@{DB_HOST}/{DB_NAME}"
engine = create_engine(connection_string)
# Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

print("Init")

def add_item_to_database(new_play: Play):
    session = Session()
    try:
        session.add(new_play)
        session.commit()
        print(f"{Fore.green}The play {Style.bold}[{new_play.name}]{Style.reset}{Fore.green} has added to DB.{Style.reset}")
    except Exception as e:
        session.rollback()
        print(f"{Fore.red}Error! Something went wrong during adding to DB: {e}. The transaction is rolled back.{Style.reset}")
    finally:
        session.close()

    # plays = session.query(Play).all()

# for play in plays:
#     print(play.id, play.name, play.s3_key)
#
# session.close()