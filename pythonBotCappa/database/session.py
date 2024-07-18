from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.setting import get_config


config = get_config()

username = config["SQLAlchemy"]["username"]
password = config["SQLAlchemy"]["password"]
db_name = config["SQLAlchemy"]["db_name"]

connection_string = f"postgresql://{username}:{password}@localhost/{db_name}"

engine = create_engine(connection_string, echo=False)
Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

