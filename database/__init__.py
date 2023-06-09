from pony.orm import Database, db_session

from config import Config

cfg = Config()

db = Database()
db.bind(provider=cfg.database_engine, filename=cfg.database_name, create_db=True)

session = db_session()

from database.models import *

db.generate_mapping(create_tables=True)