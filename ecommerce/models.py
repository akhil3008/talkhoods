from datetime import datetime
from ecommerce import db

db.Model.metadata.reflect(db.engine)


class User(db.Model):
    __table_args__ = {'extend_existing': True}
    userid = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    active = db.Column(db.Integer, default=1)
    address = db.Column(db.String(100), unique=False, nullable=False)
    city = db.Column(db.String(100), unique=False, nullable=False)
    state = db.Column(db.String(100), unique=False, nullable=False)
    country = db.Column(db.String(100), unique=False, nullable=False)
    zipcode = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    isadmin = db.Column(db.Integer, default=0)
    created_on = db.Column(db.String(25))

    def __repr__(self):
        return f"User('{self.fname}', '{self.lname}'), '{self.password}', " \
               f"'{self.address}', '{self.city}', '{self.state}', '{self.country}'," \
               f"'{self.zipcode}','{self.email}','{self.phone}')"


class user_talks(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(1000), nullable=False)
    survey_start_place = db.Column(db.String(50))
    name = db.Column(db.String(50))
    user_mobile_number = db.Column(db.String(12))
    email = db.Column(db.String(100))
    village_name = db.Column(db.String(100))
    constituency = db.Column(db.String(100))
    state = db.Column(db.String(100))
    caste = db.Column(db.String(1000))
    occupation = db.Column(db.String(100))
    aadharcard = db.Column(db.String(100))
    rationcard = db.Column(db.String(100))
    rationcard_update = db.Column(db.String(100))
    supporting_party = db.Column(db.String(100))
    roads = db.Column(db.String(100))
    drinage = db.Column(db.String(100))
    grave_yards = db.Column(db.String(100))
    water = db.Column(db.String(100))
    houses = db.Column(db.String(100))
    land_allotments = db.Column(db.String(100))
    current_mla = db.Column(db.String(100))
    number_of_visits_current = db.Column(db.Integer, default=0)
    issues = db.Column(db.String(1000))
    ex_mla = db.Column(db.String(100))
    number_of_visits_ex = db.Column(db.Integer, default=0)
    future_contestents = db.Column(db.String(200))
    expectations = db.Column(db.String(500))
    head_of_each_caste_name = db.Column(db.String(200))
    caste_head_mobile_number = db.Column(db.String(12))
    survey_taken_by = db.Column(db.String(200))
    created_on = db.Column(db.DateTime)

    def __repr__(self):
        return f"user_talks('{self.survey_start_place}','{self.name}','{self.user_mobile_number}', \
        '{self.email}',  '{self.village_name}','{self.constituency}', '{self.caste}', \
        '{self.occupation}','{self.aadharcard}','{self.rationcard}','{self.rationcard_update}', \
        '{self.supporting_party}', '{self.roads}','{self.drinage}','{self.grave_yards}',\
        '{self.water}','{self.houses}','{self.land_allotments}','{self.current_mla}', \
        '{self.number_of_visits_current}','{self.issues}','{self.ex_mla}','{self.number_of_visits_ex}', \
        '{self.future_contestents}','{self.expectations}','{self.head_of_each_caste_name}',\
        '{self.caste_head_mobile_number}','{self.survey_taken_by}','{self.created_on}')"

class scheme_benefits(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    participant_name = db.Column(db.String(100))
    state = db.Column(db.String(100))
    scheme = db.Column(db.Integer)
    eligible = db.Column(db.String(3))
    received = db.Column(db.String(3))
    benefits = db.Column(db.String(1000))
    benefits_other = db.Column(db.String(1000))
    remarks = db.Column(db.String(1000))

    def __repr__(self):
        return f"scheme_benefits('{self.participant_name}','{self.state}',,'{self.scheme}', \
        '{self.eligible}', '{self.received}',  '{self.benefits},  '{self.benefits_other},  '{self.remarks}')"

class Caste(db.Model):
    __table_args__ = {'extend_existing': True}
    casteid = db.Column(db.Integer, primary_key=True)
    caste_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Category('{self.casteid}', '{self.caste_name}')"