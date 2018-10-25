from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import datetime


date_str = datetime.datetime.now().strftime("%d-%b-%Y")
#https://docs.sqlalchemy.org/en/latest/core/engines.html
engine = create_engine(
    'sqlite:///studies_db_{}.sqlite3'.format(date_str)
    )
Session = sessionmaker(bind=engine)

Base = declarative_base()