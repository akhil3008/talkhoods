import os
import secrets
import Image
from sqlalchemy.sql.functions import now

from ecommerce import app
from ecommerce.forms import *
from plotly.offline import plot
import plotly.graph_objs as go
from flask import Markup, flash
from ecommerce.models import *
from flask import Flask, Response, render_template, request
import json
import requests
import yaml

loadapi = yaml.safe_load(open('config.yaml'))

@app.route("/", methods=['GET'])
def home():
    return render_template('login.html')

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if is_valid(email, password):
            session['email'] = email
            if isUserAdmin():
                # Return to admin page
                return redirect('admin')
            return redirect(url_for('admin'))
        else:
            error = 'Invalid UserId / Password'
            return render_template('login.html', error=error)


@app.route("/logout")
def logout():
    session.pop('email', None)
    session.pop('firstname', None)
    return redirect(url_for('home'))


@app.route("/registerationForm")
def registrationForm():
    return render_template("register.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Parse form data
        msg = extractAndPersistUserDataFromForm(request)
        if msg:
            # return render_template('index.html', error=msg)
            flash('Registered Successfully', 'success')
            return redirect(url_for('home'))
        else:
            return render_template('index.html', error="Registration failed")


@app.route("/", methods=['GET'])
@app.route("/home", methods=['GET'])
def root():
    loggedIn, firstName = getLoginUserDetails()
    session['firstname'] = firstName

    if loggedIn:
        userid = getUserId()
        return render_template('index.html')
    else:
        return render_template('admin.html')





# yet to be added
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    image_path = "/tmp/"
    os.mkdir(image_path)
    picture_path = os.path.join(f"{image_path}, picture_fn")
    picture_path1 = os.path.join('/', picture_fn)
    print(picture_path)
    print(picture_path1)

    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    i.save(picture_path1)

    return picture_fn


@app.route("/admin", methods=['GET'])
def admin():
    return render_template('admin.html')


@app.route("/admin/userregistration", methods=['GET'])
def registerUser():
    if isUserAdmin():
        return render_template('registerUser.html')
    return redirect(url_for('root'))

@app.route("/admin/user/new", methods=['GET', 'POST'])
def addUser():
    if isUserAdmin():
        form = addUserForm()
        form.category.choices = [(row.casteid, row.caste_name) for row in Caste.query.all()]
        if form.image.data:
            icon = save_picture(form.image.data)
        if form.validate_on_submit():
            if form.number_of_visits_current.data == "":
                form.number_of_visits_current.data = 0

            if form.number_of_visits_ex.data == "":
                form.number_of_visits_ex.data = 0

            userdata = user_talks(image=icon,survey_start_place=form.survey_start_place.data, name=form.name.data,
                                  user_mobile_number=form.user_mobile_number.data, email=form.email.data,
                                  village_name=form.village_name.data, constituency=form.constituency.data,
                                  state=form.state.data, caste=form.category.data,
                                  occupation=form.occupation.data,aadharcard=form.aadharcard.data,
                                  rationcard=form.rationcard.data,rationcard_update=form.rationcard_update.data,
                                  supporting_party=form.supporting_party.data,
                                  roads=form.roads.data, drinage=form.drinage.data, grave_yards=form.grave_yards.data,
                                  water=form.water.data, houses=form.houses.data,
                                  land_allotments=form.land_allotments.data, current_mla=form.current_mla.data,
                                  number_of_visits_current=form.number_of_visits_current.data,
                                  issues=form.issues.data, ex_mla=form.ex_mla.data,
                                  number_of_visits_ex=form.number_of_visits_ex.data,
                                  future_contestents=form.future_contestents.data, expectations=form.expectations.data,
                                  head_of_each_caste_name=form.head_of_each_caste_name.data,
                                  caste_head_mobile_number=form.caste_head_mobile_number.data, survey_taken_by=session['email'],
                                  created_on=now())
            db.session.add(userdata)
            db.session.commit()

            session['participant_name'] = form.name.data
            if session['participant_name'] == "":
                session['participant_name'] = form.name.data
            else:
                session.pop('participant_name', None)
                session['participant_name'] = form.name.data

            session['state'] = form.state.data
            if session['state'] == "":
                session['state'] = form.state.data
            else:
                session.pop('state', None)
                session['state'] = form.state.data

            flash(f'user_talks {form.name} added successfully', 'success')
            # return render_template("admin.html")
            return redirect(url_for('addSchemes'))
        return render_template("addUser.html", form=form, legend="New Product")
    return redirect(url_for('root'))


@app.route("/admin/user/schemes", methods=['GET', 'POST'])
def addSchemes():
    if isUserAdmin():
        if session['state'] == "2":
            form = addschemeForm()
            if form.validate_on_submit():
                scheme1_userdata = scheme_benefits(participant_name=session['participant_name'], state=session['state'],
                                                   scheme=1, eligible=form.scheme1.data,
                                                   received=form.scheme1_received.data,
                                                   benefits=form.scheme1_benefits.data,
                                                   benefits_other=form.scheme1_benefits_other.data,
                                                   remarks=form.scheme1_remarks.data)
                scheme2_userdata = scheme_benefits(participant_name=session['participant_name'], state=session['state'],
                                                   scheme=2, eligible=form.scheme2.data,
                                                   received=form.scheme2_received.data,
                                                   benefits=form.scheme2_benefits.data,
                                                   benefits_other=form.scheme2_benefits_other.data,
                                                   remarks=form.scheme2_remarks.data)
                scheme3_userdata = scheme_benefits(participant_name=session['participant_name'], state=session['state'],
                                                   scheme=3, eligible=form.scheme3.data,
                                                   received=form.scheme3_received.data,
                                                   benefits=form.scheme3_benefits.data,
                                                   benefits_other=form.scheme3_benefits_other.data,
                                                   remarks=form.scheme3_remarks.data)
                scheme4_userdata = scheme_benefits(participant_name=session['participant_name'], state=session['state'],
                                                   scheme=4, eligible=form.scheme4.data,
                                                   received=form.scheme4_received.data,
                                                   benefits=form.scheme4_benefits.data,
                                                   benefits_other=form.scheme4_benefits_other.data,
                                                   remarks=form.scheme4_remarks.data)
                scheme5_userdata = scheme_benefits(participant_name=session['participant_name'], state=session['state'],
                                                   scheme=5, eligible=form.scheme5.data,
                                                   received=form.scheme5_received.data,
                                                   benefits=form.scheme5_benefits.data,
                                                   benefits_other=form.scheme5_benefits_other.data,
                                                   remarks=form.scheme5_remarks.data)
                db.session.add(scheme1_userdata)
                db.session.commit()
                db.session.add(scheme2_userdata)
                db.session.commit()
                db.session.add(scheme3_userdata)
                db.session.commit()
                db.session.add(scheme4_userdata)
                db.session.commit()
                db.session.add(scheme5_userdata)
                db.session.commit()

                schemes_data_dict = {}
                scheme1_data_dict = {}
                scheme2_data_dict = {}
                scheme3_data_dict = {}
                scheme4_data_dict = {}
                scheme5_data_dict = {}
                scheme_data_dict = {}

                schemes_data_dict["1"] = "Annadata Sukhibava"
                schemes_data_dict["2"] = "Pasupu Kunkuma"
                schemes_data_dict["3"] = "Pensioners"
                schemes_data_dict["4"] = "Ammaki Vandanam"
                schemes_data_dict["5"] = "Unemployment"
                scheme_data_dict["1"] = "Yes"
                scheme_data_dict["0"] = "No"

                scheme1_data_dict["eligible"] = form.scheme1.data
                scheme1_data_dict["received"] = form.scheme1_received.data
                scheme1_data_dict["benefits"] = int(form.scheme1_benefits.data)
                scheme1_data_dict["benefits_other"] = int(form.scheme1_benefits_other.data)
                scheme1_data_dict["diff"] = scheme1_data_dict["benefits"] - scheme1_data_dict["benefits_other"]
                scheme2_data_dict["eligible"] = form.scheme2.data
                scheme2_data_dict["received"] = form.scheme2_received.data
                scheme2_data_dict["benefits"] = int(form.scheme2_benefits.data)
                scheme2_data_dict["benefits_other"] = int(form.scheme2_benefits_other.data)
                scheme2_data_dict["diff"] = scheme2_data_dict["benefits"] - scheme2_data_dict["benefits_other"]
                scheme3_data_dict["eligible"] = form.scheme3.data
                scheme3_data_dict["received"] = form.scheme3_received.data
                scheme3_data_dict["benefits"] = int(form.scheme3_benefits.data)
                scheme3_data_dict["benefits_other"] = int(form.scheme3_benefits_other.data)
                scheme3_data_dict["diff"] = scheme3_data_dict["benefits"] - scheme3_data_dict["benefits_other"]
                scheme4_data_dict["eligible"] = form.scheme4.data
                scheme4_data_dict["received"] = form.scheme4_received.data
                scheme4_data_dict["benefits"] = int(form.scheme4_benefits.data)
                scheme4_data_dict["benefits_other"] = int(form.scheme4_benefits_other.data)
                scheme4_data_dict["diff"] = scheme4_data_dict["benefits"] - scheme4_data_dict["benefits_other"]
                scheme5_data_dict["eligible"] = form.scheme5.data
                scheme5_data_dict["received"] = form.scheme5_received.data
                scheme5_data_dict["benefits"] = int(form.scheme5_benefits.data)
                scheme5_data_dict["benefits_other"] = int(form.scheme5_benefits_other.data)
                scheme5_data_dict["diff"] = scheme5_data_dict["benefits"] - scheme5_data_dict["benefits_other"]

                return render_template("projectSchemesData.html", scheme_data_dict=scheme_data_dict, schemes_data_dict=schemes_data_dict, scheme1_data_dict=scheme1_data_dict, scheme2_data_dict=scheme2_data_dict, scheme3_data_dict=scheme3_data_dict, scheme4_data_dict=scheme4_data_dict, scheme5_data_dict=scheme5_data_dict)
        else:
            form = addschemeFormTS()
            if form.validate_on_submit():
                scheme1_userdata = scheme_benefits(participant_name=session['participant_name'], state=session['state'],
                                                   scheme=1,
                                                   eligible=form.scheme1.data,
                                                   received=form.scheme1_received.data,
                                                   benefits=form.scheme1_benefits.data,
                                                   remarks=form.scheme1_remarks.data)
                scheme2_userdata = scheme_benefits(participant_name=session['participant_name'], state=session['state'],
                                                   scheme=2,
                                                   eligible=form.scheme2.data,
                                                   received=form.scheme2_received.data,
                                                   benefits=form.scheme2_benefits.data,
                                                   remarks=form.scheme2_remarks.data)
                scheme3_userdata = scheme_benefits(participant_name=session['participant_name'], state=session['state'],
                                                   scheme=3,
                                                   eligible=form.scheme3.data,
                                                   received=form.scheme3_received.data,
                                                   benefits=form.scheme3_benefits.data,
                                                   remarks=form.scheme3_remarks.data)
                scheme4_userdata = scheme_benefits(participant_name=session['participant_name'], state=session['state'],
                                                   scheme=4,
                                                   eligible=form.scheme4.data,
                                                   received=form.scheme4_received.data,
                                                   benefits=form.scheme4_benefits.data,
                                                   remarks=form.scheme4_remarks.data)
                scheme5_userdata = scheme_benefits(participant_name=session['participant_name'], state=session['state'],
                                                   scheme=5,
                                                   eligible=form.scheme5.data,
                                                   received=form.scheme5_received.data,
                                                   benefits=form.scheme5_benefits.data,
                                                   remarks=form.scheme5_remarks.data)
                db.session.add(scheme1_userdata)
                db.session.commit()
                db.session.add(scheme2_userdata)
                db.session.commit()
                db.session.add(scheme3_userdata)
                db.session.commit()
                db.session.add(scheme4_userdata)
                db.session.commit()
                db.session.add(scheme5_userdata)
                db.session.commit()
                schemes_data_dict = {}
                scheme1_data_dict = {}
                scheme2_data_dict = {}
                scheme3_data_dict = {}
                scheme4_data_dict = {}
                scheme5_data_dict = {}
                scheme_data_dict = {}

                schemes_data_dict["1"] = "KCR Kit"
                schemes_data_dict["2"] = "Arogya Lakshmi"
                schemes_data_dict["3"] = "Aasara pensions"
                schemes_data_dict["4"] = "Housing for the poor"
                schemes_data_dict["5"] = "Unemployment"
                scheme_data_dict["1"] = "Yes"
                scheme_data_dict["0"] = "No"

                scheme1_data_dict["eligible"] = form.scheme1.data
                scheme1_data_dict["received"] = form.scheme1_received.data
                scheme1_data_dict["benefits"] = int(form.scheme1_benefits.data)
                scheme1_data_dict["benefits_other"] = int(form.scheme1_benefits_other.data)
                scheme1_data_dict["diff"] = scheme1_data_dict["benefits"] - scheme1_data_dict["benefits_other"]
                scheme2_data_dict["eligible"] = form.scheme2.data
                scheme2_data_dict["received"] = form.scheme2_received.data
                scheme2_data_dict["benefits"] = int(form.scheme2_benefits.data)
                scheme2_data_dict["benefits_other"] = int(form.scheme2_benefits_other.data)
                scheme2_data_dict["diff"] = scheme2_data_dict["benefits"] - scheme2_data_dict["benefits_other"]
                scheme3_data_dict["eligible"] = form.scheme3.data
                scheme3_data_dict["received"] = form.scheme3_received.data
                scheme3_data_dict["benefits"] = int(form.scheme3_benefits.data)
                scheme3_data_dict["benefits_other"] = int(form.scheme3_benefits_other.data)
                scheme3_data_dict["diff"] = scheme3_data_dict["benefits"] - scheme3_data_dict["benefits_other"]
                scheme4_data_dict["eligible"] = form.scheme4.data
                scheme4_data_dict["received"] = form.scheme4_received.data
                scheme4_data_dict["benefits"] = int(form.scheme4_benefits.data)
                scheme4_data_dict["benefits_other"] = int(form.scheme4_benefits_other.data)
                scheme4_data_dict["diff"] = scheme4_data_dict["benefits"] - scheme4_data_dict["benefits_other"]
                scheme5_data_dict["eligible"] = form.scheme5.data
                scheme5_data_dict["received"] = form.scheme5_received.data
                scheme5_data_dict["benefits"] = int(form.scheme5_benefits.data)
                scheme5_data_dict["benefits_other"] = int(form.scheme5_benefits_other.data)
                scheme5_data_dict["diff"] = scheme5_data_dict["benefits"] - scheme5_data_dict["benefits_other"]

                return render_template("projectSchemesData.html", scheme_data_dict=scheme_data_dict, schemes_data_dict=schemes_data_dict, scheme1_data_dict=scheme1_data_dict, scheme2_data_dict=scheme2_data_dict, scheme3_data_dict=scheme3_data_dict, scheme4_data_dict=scheme4_data_dict, scheme5_data_dict=scheme5_data_dict)
        return render_template("addSchemes.html", form=form, legend="Schemes")
    return redirect(url_for('root'))




@app.route("/admin/users", methods=['GET'])
def getUsers():
    if isUserAdmin():
        cur = mysql.connection.cursor()
        cur.execute(
            'SELECT u.fname, u.lname, u.email, u.active, u.city, u.state, COUNT(o.orderid) as noOfOrders FROM `user` u LEFT JOIN `order` o ON u.userid = o.userid GROUP BY u.userid')
        users = cur.fetchall()
        return render_template('adminUsers.html', users=users)
    return redirect(url_for('root'))


@app.route("/profile", methods=['GET', 'POST'])
def profile():
    loggedIn, firstName = getLoginUserDetails()
    return render_template('404.html', loggedIn=loggedIn, firstName=firstName)

@app.route("/forgotPassword", methods=['GET', 'POST'])
def forgotPassword():
    loggedIn, firstName, productCountinKartForGivenUser = getLoginUserDetails()
    return render_template('404.html', loggedIn=loggedIn, firstName=firstName)


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
    if 'email' not in session:
        loggedIn = False
        firstName = ''
    else:
        loggedIn = True
        userid, firstName = User.query.with_entities(User.userid, User.fname).filter(
            User.email == session['email']).first()

    return (loggedIn, firstName)

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
                city=city, state=state, country=country, zipcode=zipcode, email=email, phone=phone, isadmin=1)

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


# check if user is an admin
def isUserAdmin():
    if isUserLoggedIn():
        userId = User.query.with_entities(User.userid).filter(User.email == session['email']).first()
        # print(UserId)
        currentUser = User.query.get_or_404(userId)
        return currentUser.isadmin