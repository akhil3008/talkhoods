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





def is_valid(email, password):
    # Using Flask-SQLAlchmy ORM
    # data = User.query.with_entities(User.email, User.password).all()

    # Using Raw SQL Select Query
    cur = mysql.connection.cursor()
    cur.execute("SELECT email, password FROM user")
    userData = cur.fetchall()
    cur.close()

    for row in userData:
        if row['email'] == email and row['password'] == hashlib.md5(password.encode()).hexdigest():
            return True
    return False


def getLoginUserDetails():
    productCountinCartForGivenUser = 0

    if 'email' not in session:
        loggedIn = False
        firstName = ''
    else:
        loggedIn = True
        userid, firstName = User.query.with_entities(User.userid, User.fname).filter(
            User.email == session['email']).first()

        productCountinCart = []

        # for Cart in Cart.query.filter(Cart.userId == userId).distinct(Products.productId):
        for cart in Cart.query.filter(Cart.userid == userid).all():
            productCountinCart.append(cart.productid)
            productCountinCartForGivenUser = len(productCountinCart)

    return (loggedIn, firstName, productCountinCartForGivenUser)

def getUserId():


    if 'email' not in session:
        userid = 10009
    else:
        userid = User.query.with_entities(User.userid).filter(
            User.email == session['email']).first()
    userId = userid[0]
    return userId



def extractAndPersistUserDataFromForm(request):
    password = request.form['password']
    email = request.form['email']
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    address = request.form['address']
    zipcode = request.form['zipcode']
    city = request.form['city']
    state = request.form['state']
    country = request.form['country']
    phone = request.form['phone']

    user = User(fname=firstName, lname=lastName, password=hashlib.md5(password.encode()).hexdigest(), address=address,
                city=city, state=state, country=country, zipcode=zipcode, email=email, phone=phone)

    try:
        db.session.add(user)
        db.session.flush()
        db.session.commit()
    except exc.SQLAlchemyError:
        return "Registration failed"
    return "Registered Successfully"


def isUserLoggedIn():
    if 'email' not in session:
        return False
    else:
        return True


# check if user is an admin.html
def isUserAdmin():
    if isUserLoggedIn():
        # ProductCategory.query.filter_by(productid=product.productid).first()
        userId = User.query.with_entities(User.userid).filter(User.email == session['email']).first()
        currentUser = User.query.get_or_404(userId)
        return currentUser.isadmin

class addUserForm(FlaskForm):
    survey_start_place = StringField('Survey Place:', validators=[DataRequired()])
    name = StringField('Name:', validators=[DataRequired()])
    user_mobile_number = IntegerField('Mobile Number:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired()])
    village_name = StringField('Village Name:', validators=[DataRequired()])
    constituency = StringField('Constituency:', validators=[DataRequired()])
    category = SelectField('Caste:', coerce=int, id='select_category')
    occupation = StringField('Occupation:', validators=[DataRequired()])
    supporting_party = StringField('Supporting Party:', validators=[DataRequired()])
    roads = StringField('Roads:', validators=[DataRequired()])
    drinage = StringField('Drinage:', validators=[DataRequired()])
    grave_yards = StringField('Grave Yards:', validators=[DataRequired()])
    water = StringField('Water:', validators=[DataRequired()])
    houses = StringField('Houses:', validators=[DataRequired()])
    land_allotments = StringField('Land Allotments:', validators=[DataRequired()])
    current_mla = StringField('Current MLA:', validators=[DataRequired()])
    number_of_visits_current = IntegerField('Number of Visits:', validators=[DataRequired()])
    ex_mla = StringField('Ex MLA:', validators=[DataRequired()])
    number_of_visits_ex = IntegerField('Number of Visits Ex MLA:', validators=[DataRequired()])
    future_contestents = StringField('Future Contestents:', validators=[DataRequired()])
    expectations = StringField('Expectations:', validators=[DataRequired()])
    head_of_each_caste_name = StringField('Head of each Caste Name:', validators=[DataRequired()])
    caste_head_mobile_number = IntegerField('Caste Head Mobile Number:', validators=[DataRequired()])
    submit = SubmitField('Save')

class addschemeForm(FlaskForm):
    scheme1 = SelectField('Annadata Sukhibava Eligible:', choices=[(1, 'Yes'), (2, 'No')])
    scheme1_received = SelectField('Received:', choices=[(1, 'Yes'), (2, 'No')])
    scheme1_benefits = StringField('Benefits:')
    scheme2 = SelectField('Pasupu Kunkuma Eligible:', choices=[(1, 'Yes'), (2, 'No')])
    scheme2_received = SelectField('Received:', choices=[(1, 'Yes'), (2, 'No')])
    scheme2_benefits = StringField('Benefits:')
    scheme3 = SelectField('Pensioners Eligible:', choices=[(1, 'Yes'), (2, 'No')])
    scheme3_received = SelectField('Received:', choices=[(1, 'Yes'), (2, 'No')])
    scheme3_benefits = StringField('Benefits:')
    scheme4 = SelectField('Ammaki Vandanam Eligible:', choices=[(1, 'Yes'), (2, 'No')])
    scheme4_received = SelectField('Received:', choices=[(1, 'Yes'), (2, 'No')])
    scheme4_benefits = StringField('Benefits:')
    scheme5 = SelectField('Unemployment Eligible:', choices=[(1, 'Yes'), (2, 'No')])
    scheme5_received = SelectField('Received:', choices=[(1, 'Yes'), (2, 'No')])
    scheme5_benefits = StringField('Benefits:')
    submit = SubmitField('Save')
