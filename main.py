print("Hello")

PATH_TO_XML_FILES = r"c:\\Dev\\06. Data\\1. XML from FDA\\03.1 test XML data from FDA\\"

from sqlalchemy_base import Base,  engine, Session

from data_models import Actor
from datetime import date


# 2 - generate database schema
Base.metadata.create_all(engine)

# 3 - create a new session
session = Session()

matt_damon = Actor("Matt Damon", date(1970, 10, 8))

session.add(matt_damon)

# 10 - commit and close session
session.commit()
session.close()
