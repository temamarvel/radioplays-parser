import os
from math import trunc

from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, UniqueConstraint
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import sessionmaker
from colored import Fore, Back, Style

from db_models import Play, S3File, Base, PlayInfo

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

connection_string = f"postgresql://{DB_USER}:@{DB_HOST}/{DB_NAME}"
engine = create_engine(connection_string)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

print("Init")

# Типизация: только Play или S3File
def add_item_to_database(obj: Play or S3File or PlayInfo):
    session = Session()
    try:
        model_class = type(obj)

        data = {
            column.key: getattr(obj, column.key)
            for column in inspect(obj).mapper.column_attrs
            if column.key != "id"
        }

        table_args = getattr(model_class, "__table_args__", [])
        if not isinstance(table_args, (list, tuple)):
            table_args = [table_args]

        constraint_name = None
        for arg in table_args:
            if isinstance(arg, UniqueConstraint) and arg.name:
                constraint_name = arg.name
                break

        if not constraint_name:
            raise ValueError(f"No named UniqueConstraint found in model {model_class.__name__}")


        stmt = (
            insert(model_class)
            .values(**data)
            .on_conflict_do_nothing(constraint=constraint_name)
            .returning(model_class.id)
        )

        result = session.execute(stmt).scalar()

        if result:
            session.commit()
            print(f"{Fore.green}✅ Added to {model_class.__name__}: {data}{Style.reset}")
        else:
            print(f"{Fore.yellow}⚠️ Duplicate in {model_class.__name__}, not added: {data}{Style.reset}")

        return result
    except Exception as e:
        session.rollback()
        print(f"{Fore.red}❌ Error adding {model_class.__name__}: {e}{Style.reset}")
        return None
    finally:
        session.close()

    # plays = session.query(Play).all()

def is_play_in_database(play: Play):
    session = Session()
    try:
        record = session.query(Play).filter(Play.s3_prefix == play.s3_prefix).first()
        if record:
            print(f"{Fore.green}The item {Style.bold}[{play.s3_prefix}]{Style.reset}{Fore.green} is in DB.{Style.reset}")
            return True
        else:
            print(f"{Fore.red}The item {Style.bold}[{play.s3_prefix}]{Style.reset}{Fore.red} isn't found in DB.{Style.reset}")
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