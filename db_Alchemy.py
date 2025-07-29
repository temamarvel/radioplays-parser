import os
from math import trunc

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.dialects.mssql.information_schema import constraints
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import sessionmaker, declarative_base
from colored import Fore, Back, Style

from db_models import Play, Base

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
        stmt = (insert(Play).values(title=new_play.title, name=new_play.name, s3_folder_key=new_play.s3_folder_key)
                .on_conflict_do_nothing(constraint='uq_name')
                .returning(Play.id))
        # session.add(new_play)
        result = session.execute(stmt).scalar()
        if result:
            session.commit()
            print(f"{Fore.green}The play {Style.bold}[{new_play.name}]{Style.reset}{Fore.green} has added to DB.{Style.reset}")
        else:
            print(f"{Fore.red}Duplicate! The play {Style.bold}[{new_play.name}]{Style.reset}{Fore.red} hasn't been added to DB.{Style.reset}")
    except Exception as e:
        session.rollback()
        print(f"{Fore.red}Error! Something went wrong during adding to DB: {e}. The transaction is rolled back.{Style.reset}")
    finally:
        session.close()

    # plays = session.query(Play).all()

def is_play_in_database(play: Play):
    session = Session()
    try:
        record = session.query(Play).filter(Play.s3_folder_key == play.s3_folder_key).first()
        if record:
            print(f"{Fore.green}The item {Style.bold}[{play.s3_folder_key}]{Style.reset}{Fore.green} is in DB.{Style.reset}")
            return True
        else:
            print(f"{Fore.red}The item {Style.bold}[{play.s3_folder_key}]{Style.reset}{Fore.red} isn't found in DB.{Style.reset}")
            return False
    except Exception as e:
        session.rollback()
        print(f"{Fore.red}Error! Something went wrong during checking existence to DB: {e}. The transaction is rolled back.{Style.reset}")
    finally:
        session.close()

    return False

# for play in plays:
#     print(play.id, play.name, play.s3_key)
#
# session.close()