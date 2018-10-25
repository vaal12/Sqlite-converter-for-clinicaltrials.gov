from sqlalchemy import Column, String, Integer, Date
from sqlalchemy_base import Base


class Study(Base):
    __tablename__ = 'studies'

    id = Column(Integer, primary_key=True)

    nct_id 	 = Column(String, 	doc = "id_info > nct_id")
    
    allocation	 = Column(String, 	doc = "study_design_info > allocation")
    brief_summary 	 = Column(String, 	doc = "brief_summary > textblock")
    brief_title 	 = Column(String, 	doc = "brief_title")
    completion_date	 = Column(String, 	doc = "completion_date")
    detailed_description 	 = Column(String, 	doc = "detailed_description > textblock")
    has_expanded_access 	 = Column(String, 	doc = "has_expanded_access")
    intervention_model 	 = Column(String, 	doc = "study_design_info > intervention_model")
    last_known_status	 = Column(String, 	doc = "last_known_status")
    last_update_submitted	 = Column(String, 	doc = "last_update_submitted")
    masking 	 = Column(String, 	doc = "study_design_info > masking")
    
    official_title	 = Column(String, 	doc = "official_title")
    org_study_id	 = Column(String, 	doc = "id_info > org_study_id")
    overall_status 	 = Column(String, 	doc = "overall_status")
    phase	 = Column(String, 	doc = "phase")
    primary_purpose 	 = Column(String, 	doc = "study_design_info > primary_purpose")
    source 	 = Column(String, 	doc = "source")
    start_date	 = Column(String, 	doc = "start_date")
    study_first_submitted	 = Column(String, 	doc = "study_first_submitted")
    study_first_submitted_qc	 = Column(String, 	doc = "study_first_submitted_qc")
    study_type 	 = Column(String, 	doc = "study_type")
    url	 = Column(String, 	doc = "required_header > url")

    def __init__(self):
        pass
#END class Study(Base):

class LocationCountry(Base):
    __tablename__ = 'location_countries'

    id = Column(Integer, primary_key=True)
    nct_id	 = Column(String, 	doc = "id_info > nct_id")
    country	 = Column(String, 	doc = "location_countries > country")

    def __init__(self):
        pass
#END class LocationCountry(Base):




# class Actor(Base):
#     __tablename__ = 'actors'

#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     birthday = Column(Date)

#     def __init__(self, name, birthday):
#         self.name = name
#         self.birthday = birthday