print("Hello")

PATH_TO_XML_FILES = r"c:\\Dev\\06. Data\\1. XML from FDA\\03.1 test XML data from FDA\\"

from sqlalchemy_base import Base,  engine, Session
import sqlalchemy.orm.attributes

from data_models import Study, LocationCountry
from datetime import date



# 2 - generate database schema
Base.metadata.create_all(engine)

# 3 - create a new session
session = Session()

# matt_damon = Actor("Matt Damon", date(1970, 10, 8))

new_study = Study()

studies_field_list = [col for col in dir(Study) if type(getattr(Study, col)) is (sqlalchemy.orm.attributes.InstrumentedAttribute)]
print("Field list: \n{}".format(studies_field_list))

studies_field_doc_strs = [getattr(getattr(Study, col), "doc") for col in studies_field_list ]

print studies_field_doc_strs

for field in studies_field_list:
    if field <> "id":
        setattr(new_study, field, "I am a field:"+field)

session.add(new_study)

# session.add(matt_damon)

# 10 - commit and close session
session.commit()
session.close()
