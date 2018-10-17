from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


#https://docs.sqlalchemy.org/en/latest/core/engines.html
engine = create_engine(
    'sqlite:///c:\\Dev\\04. Python\\04. Sqlite converter for FDA list\\db_1.sqlite3'
    )
Session = sessionmaker(bind=engine)

Base = declarative_base()