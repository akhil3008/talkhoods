import hashlib

from flask import session
from flask import url_for, flash, redirect
from flask_wtf import FlaskForm
from sqlalchemy import func, exc

from wtforms import StringField, SubmitField, TextAreaField, IntegerField, RadioField, FloatField, SelectField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email

from ecommerce import mysql
from ecommerce.models import *




class addUserForm(FlaskForm):
    survey_start_place = StringField('Survey Place:')
    name = StringField('Name:', validators=[DataRequired()])
    user_mobile_number = StringField('Mobile Number:')
    email = StringField('Email:')
    village_name = StringField('Village Name:')
    constituency = StringField('Constituency:')
    state = SelectField('State:', choices=[(1, 'Telangana'), (2, 'Andhra Pradesh')])
    category = SelectField('Caste:', coerce=int, id='select_category')
    occupation = StringField('Occupation:')
    aadharcard = StringField('Aadhar Card:')
    rationcard = SelectField('Ration Card:', choices=[(1, 'Yes'), (0, 'No')])
    rationcard_update = StringField('If No, Provide details of removal/ Not received')
    supporting_party = StringField('Supporting Party:')
    roads = StringField('Roads:')
    drinage = StringField('Drinage:')
    grave_yards = StringField('Grave Yards:')
    water = StringField('Water:')
    houses = StringField('Houses:')
    land_allotments = StringField('Land Allotments:')
    current_mla = StringField('Current MLA:')
    number_of_visits_current = StringField('Number of Visits:')
    issues = StringField('Issues:')
    ex_mla = StringField('Ex MLA:')
    number_of_visits_ex = StringField('Number of Visits Ex MLA:')
    future_contestents = StringField('Future Contestents:')
    expectations = StringField('Expectations:')
    head_of_each_caste_name = StringField('Head of each Caste Name:')
    caste_head_mobile_number = StringField('Caste Head Mobile Number:')
    submit = SubmitField('Save')

class addschemeForm(FlaskForm):
    scheme1 = SelectField('Annadata Sukhibava:', choices=[(1, 'Yes'), (0, 'No')])
    scheme1_received = SelectField('Received:', choices=[(1, 'Yes'), (0, 'No')])
    scheme1_benefits = StringField('Benefits:')
    scheme1_benefits_other = StringField('Benefits_other:')
    scheme2 = SelectField('Pasupu Kunkuma Eligible:', choices=[(1, 'Yes'), (0, 'No')])
    scheme2_received = SelectField('Received:', choices=[(1, 'Yes'), (0, 'No')])
    scheme2_benefits = StringField('Benefits:')
    scheme2_benefits_other = StringField('Benefits_other:')
    scheme3 = SelectField('Pensioners Eligible:', choices=[(1, 'Yes'), (0, 'No')])
    scheme3_received = SelectField('Received:', choices=[(1, 'Yes'), (0, 'No')])
    scheme3_benefits = StringField('Benefits:')
    scheme3_benefits_other = StringField('Benefits_other:')
    scheme4 = SelectField('Ammaki Vandanam Eligible:', choices=[(1, 'Yes'), (0, 'No')])
    scheme4_received = SelectField('Received:', choices=[(1, 'Yes'), (0, 'No')])
    scheme4_benefits = StringField('Benefits:')
    scheme4_benefits_other = StringField('Benefits_other:')
    scheme5 = SelectField('Unemployment Eligible:', choices=[(1, 'Yes'), (0, 'No')])
    scheme5_received = SelectField('Received:', choices=[(1, 'Yes'), (0, 'No')])
    scheme5_benefits = StringField('Benefits:')
    scheme5_benefits_other = StringField('Benefits_other:')
    submit = SubmitField('Save')

class addschemeFormTS(FlaskForm):
    scheme1 = SelectField('KCR Kit:', choices=[(1, 'Yes'), (0, 'No')])
    scheme1_received = SelectField('Received:', choices=[(1, 'Yes'), (0, 'No')])
    scheme1_benefits = StringField('Benefits:')
    scheme1_benefits_other = StringField('Benefits_other:')
    scheme2 = SelectField('Arogya Lakshmi:', choices=[(1, 'Yes'), (0, 'No')])
    scheme2_received = SelectField('Received:', choices=[(1, 'Yes'), (0, 'No')])
    scheme2_benefits = StringField('Benefits:')
    scheme2_benefits_other = StringField('Benefits_other:')
    scheme3 = SelectField('Aasara pensions:', choices=[(1, 'Yes'), (0, 'No')])
    scheme3_received = SelectField('Received:', choices=[(1, 'Yes'), (0, 'No')])
    scheme3_benefits = StringField('Benefits:')
    scheme3_benefits_other = StringField('Benefits_other:')
    scheme4 = SelectField('Housing for the poor:', choices=[(1, 'Yes'), (0, 'No')])
    scheme4_received = SelectField('Received:', choices=[(1, 'Yes'), (0, 'No')])
    scheme4_benefits = StringField('Benefits:')
    scheme4_benefits_other = StringField('Benefits_other:')
    scheme5 = SelectField('Unemployment:', choices=[(1, 'Yes'), (0, 'No')])
    scheme5_received = SelectField('Received:', choices=[(1, 'Yes'), (0, 'No')])
    scheme5_benefits = StringField('Benefits:')
    scheme5_benefits_other = StringField('Benefits_other:')
    submit = SubmitField('Save')