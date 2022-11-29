import os
import secrets
import Image
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

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    products = getProductList()
    products = [value for (value,) in products]
    return Response(json.dumps(products), mimetype='application/json')


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
            return redirect(url_for('root'))
        else:
            error = 'Invalid UserId / Password'
            return render_template('index.html', error=error)


@app.route("/logout")
def logout():
    session.pop('email', None)
    session.pop('firstname', None)
    return redirect(url_for('root'))


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
            return redirect(url_for('root'))
        else:
            return render_template('index.html', error="Registration failed")


@app.route("/", methods=['GET'])
@app.route("/home", methods=['GET'])
def root():
    loggedIn, firstName, productCountinKartForGivenUser = getLoginUserDetails()
    session['firstname'] = firstName
    allProductDetails = getAllProducts()
    allProductsMassagedDetails = massageItemData(allProductDetails)
    categoryData = getCategoryDetails()

    if loggedIn:
        userid = getUserId()
        user_api_url = loadapi['userProductRecommendationServiceUrl']
        userid = {"userid": userid}
        response = requests.post(user_api_url, json=userid)
        prod_json = response.json()

        list = []
        for i in range(0, len(prod_json['Product_ids'])):
            list.append(prod_json['Product_ids'][i])

        recommendedProducts = getRecommendedProducts(list)
        recommendedProductsMassagedDetails = massageItemData(recommendedProducts)
        return render_template('index.html', itemData=allProductsMassagedDetails, loggedIn=loggedIn,
                               firstName=firstName,
                               productCountinKartForGivenUser=productCountinKartForGivenUser,
                               categoryData=categoryData, recommendedProducts=recommendedProductsMassagedDetails)
    else:
        return render_template('index.html', itemData=allProductsMassagedDetails, loggedIn=loggedIn,
                               firstName=firstName,
                               productCountinKartForGivenUser=productCountinKartForGivenUser,
                               categoryData=categoryData)


@app.route("/displayCategory")
def displayCategory():
    loggedIn, firstName, noOfItems = getLoginUserDetails()
    categoryId = request.args.get("categoryId")
    productDetailsByCategoryId = Product.query.join(ProductCategory, Product.productid == ProductCategory.productid) \
        .add_columns(Product.productid, Product.product_name, Product.regular_price, Product.discounted_price,
                     Product.image) \
        .join(Category, Category.categoryid == ProductCategory.categoryid) \
        .filter(Category.categoryid == int(categoryId)) \
        .add_columns(Category.category_name) \
        .all()

    categoryName = productDetailsByCategoryId[0].category_name
    data = massageItemData(productDetailsByCategoryId)
    return render_template('displayCategory.html', data=data, loggedIn=loggedIn, firstName=firstName,
                           noOfItems=noOfItems, categoryName=categoryName)


@app.route("/productDescription")
def productDescription():
    loggedIn, firstName, noOfItems = getLoginUserDetails()
    productid = request.args.get('productId')
    productDetailsByProductId = getProductDetails(productid)
    api_url = loadapi['recommendationServiceUrl']
    products = {"product_id": productid}
    response = requests.post(api_url, json=products)
    prod_json = response.json()
    # prod_json = {"Product_ids": [202228337, 2, 3, 4, 5]}
    list = []
    for i in range(0, len(prod_json['Product_ids'])):
        list.append(prod_json['Product_ids'][i])

    recommendedProducts = getRecommendedProducts(list)
    recommendedProductsMassagedDetails = massageItemData(recommendedProducts)

    return render_template("productDescription.html", data=productDetailsByProductId, loggedIn=loggedIn,
                           firstName=firstName, productCountinKartForGivenUser=noOfItems,
                           recommendedProducts=recommendedProductsMassagedDetails)


@app.route('/search', methods=['GET', 'POST'])
def index():
    loggedIn, firstName, productCountinKartForGivenUser = getLoginUserDetails()
    productName = request.args.get('productname')
    if productName == '':
        return redirect(url_for('root'))
    else:
        productDetailsByProductId = getProductDetailsByName(productName)
        if len(productDetailsByProductId) == 0:
            flash('No Products Found')
            return redirect(url_for('root'))
        else:
            id = productDetailsByProductId[0].productid
            api_url = loadapi['recommendationServiceUrl']
            products = {"product_id": id}
            response = requests.post(api_url, json=products)
            prod_json = response.json()
            list = []
            for i in range(0, len(prod_json['Product_ids'])):
                list.append(prod_json['Product_ids'][i])

            recommendedProducts = getRecommendedProducts(list)
            recommendedProductsMassagedDetails = massageItemData(recommendedProducts)
            return render_template("ProductSearch.html", itemData=productDetailsByProductId, loggedIn=loggedIn,
                                   firstName=firstName, productCountinKartForGivenUser=productCountinKartForGivenUser,
                                   recommendedProducts=recommendedProductsMassagedDetails)


@app.route("/addToCart", methods=['GET', 'POST'])
def addToCart():
    if isUserLoggedIn():
        product_details = request.form['weight']
        print(product_details)
        sku = product_details.split(" - ")[0]
        subproductId = product_details.split(" - ")[1]
        # Using Flask-SQLAlchmy SubQuery
        extractAndPersistKartDetailsUsingSubquery(sku, subproductId)
        # Using Flask-SQLAlchmy normal query
        # extractAndPersistKartDetailsUsingkwargs(productId)
        flash('Item successfully added to cart !!', 'success')
        return redirect(url_for('root'))
    else:
        flash('please log in !!', 'success')
        return redirect(url_for('root'))


@app.route("/addToCartProduct", methods=['GET', 'POST'])
def addToCartProduct():
    if isUserLoggedIn():
        productId = request.args.get('productId')
        subProductId = request.args.get('subProductId')
        print(session)
        extractAndPersistKartDetails(productId, subProductId)
        # Using Flask-SQLAlchmy normal query
        # extractAndPersistKartDetailsUsingkwargs(productId)
        flash('Item successfully added to cart !!', 'success')
        return redirect(url_for('root'))
    else:
        flash('please log in !!', 'success')
        return redirect(url_for('root'))


@app.route("/cart")
def cart():
    if isUserLoggedIn():
        loadapi = yaml.safe_load(open('config.yaml'))
        loggedIn, firstName, productCountinKartForGivenUser = getLoginUserDetails()
        cartdetails, totalsum, tax = getusercartdetails();

        api_url = loadapi['recommendationServiceUrl']
        products = {"product_id": 202212001}
        response = requests.post(api_url, json=products)
        print(response.json())
        prod_json = response.json()
        # prod_json = {"Product_ids": [202228337, 2, 3, 4, 5]}
        # print(response.json())
        list = []
        for i in range(0, len(prod_json['Product_ids'])):
            list.append(prod_json['Product_ids'][i])

        recommendedProducts = getRecommendedProducts(list)
        recommendedProductsMassagedDetails = massageItemData(recommendedProducts)
        return render_template("cart.html", cartData=cartdetails,
                               productCountinKartForGivenUser=productCountinKartForGivenUser, loggedIn=loggedIn,
                               firstName=firstName, totalsum=totalsum, tax=tax,
                               recommendedProducts=recommendedProductsMassagedDetails)
    else:
        return redirect(url_for('root'))


@app.route("/admin/category/<int:category_id>", methods=['GET'])
def category(category_id):
    if isUserAdmin():
        category = Category.query.get_or_404(category_id)
        return render_template('adminCategory.html', category=category)
    return redirect(url_for('root'))


@app.route("/admin/categories/new", methods=['GET', 'POST'])
def addCategory():
    if isUserAdmin():
        form = addCategoryForm()
        if form.validate_on_submit():
            category = Category(category_name=form.category_name.data)
            db.session.add(category)
            db.session.commit()
            flash(f'Category {form.category_name.data}! added successfully', 'success')
            return redirect(url_for('getCategories'))
        return render_template("addCategory.html", form=form)
    return redirect(url_for('getCategories'))


@app.route("/admin/categories/<int:category_id>/update", methods=['GET', 'POST'])
def update_category(category_id):
    if isUserAdmin():
        category = Category.query.get_or_404(category_id)
        form = addCategoryForm()
        if form.validate_on_submit():
            category.category_name = form.category_name.data
            db.session.commit()
            flash('This category has been updated!', 'success')
            return redirect(url_for('getCategories'))
        elif request.method == 'GET':
            form.category_name.data = category.category_name
        return render_template('addCategory.html', legend="Update Category", form=form)
    return redirect(url_for('getCategories'))


@app.route("/admin/category/<int:category_id>/delete", methods=['POST'])
def delete_category(category_id):
    if isUserAdmin():
        ProductCategory.query.filter_by(categoryid=category_id).delete()
        db.session.commit()
        category = Category.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()
        flash('Your category has been deleted!', 'success')
    return redirect(url_for('getCategories'))


@app.route("/admin/categories", methods=['GET'])
def getCategories():
    if isUserAdmin():
        # categories = Category.query.all()
        cur = mysql.connection.cursor()
        # Query for number of products on a category:
        cur.execute(
            'SELECT category.categoryid, category.category_name, COUNT(product_category.productid) as noOfProducts FROM category LEFT JOIN product_category ON category.categoryid = product_category.categoryid GROUP BY category.categoryid');
        categories = cur.fetchall()
        return render_template('adminCategories.html', categories=categories)
    return redirect(url_for('root'))


# this method is copied from Schafer's tutorials
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/uploads', picture_fn)

    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/admin", methods=['GET'])
def admin():
    return render_template('admin.html')


@app.route("/admin/products", methods=['GET'])
def getProducts():
    if isUserAdmin():
        products = Product.query.order_by(Product.sku, Product.sub_product_id).all()
        return render_template('adminProducts.html', products=products)
    return redirect(url_for('root'))



@app.route("/admin/userregistration", methods=['GET'])
def registerUser():
    if isUserAdmin():
        products = Product.query.order_by(Product.sku, Product.sub_product_id).all()
        return render_template('registerUser.html', products=products)
    return redirect(url_for('root'))

@app.route("/admin/user/new", methods=['GET', 'POST'])
def addUser():
    if isUserAdmin():
        form = addUserForm()
        form.category.choices = [(row.categoryid, row.category_name) for row in Category.query.all()]
        #print(form.category.choices)
        product_icon = ""  # safer way in case the image is not included in the form
        if form.validate_on_submit():
            userdata = user_talks(survey_start_place=form.survey_start_place.data, name=form.name.data,
                                  user_mobile_number=form.user_mobile_number.data, email=form.email.data,
                                  village_name=form.village_name.data, caste=form.category.data,
                                  occupation=form.occupation.data, supporting_party=form.supporting_party.data,
                                  roads=form.roads.data, drinage=form.drinage.data, grave_yards=form.grave_yards.data,
                                  water=form.water.data, houses=form.houses.data,
                                  land_allotments=form.land_allotments.data, current_mla=form.current_mla.data,
                                  number_of_visits_current=form.number_of_visits_current.data, ex_mla=form.ex_mla.data,
                                  number_of_visits_ex=form.number_of_visits_ex.data,
                                  future_contestents=form.future_contestents.data, expectations=form.expectations.data,
                                  head_of_each_caste_name=form.head_of_each_caste_name.data,
                                  caste_head_mobile_number=form.caste_head_mobile_number.data)
            db.session.add(userdata)
            db.session.commit()
            print(form.name.data)
            session['participant_name'] = form.name.data
            if session['participant_name'] == "":
                print("in If before")
                print(session['participant_name'])
                session['participant_name'] = form.name.data
                print("in If After")
            else:
                print("In Else")
                print(session['participant_name'])
                session.pop('participant_name', None)
                session['participant_name'] = form.name.data

            # product_category = ProductCategory(categoryid=form.category.data, productid=product.productid)
            # db.session.add(product_category)
            # db.session.commit()
            flash(f'user_talks {form.name} added successfully', 'success')
            return render_template("admin.html")
        return render_template("addProduct.html", form=form, legend="New Product")
    return redirect(url_for('root'))

@app.route("/admin/user/schemes", methods=['GET', 'POST'])
def addSchemes():
    if isUserAdmin():
        form = addschemeForm()
        product_icon = ""  # safer way in case the image is not included in the form
        if form.validate_on_submit():
            scheme1_userdata = scheme_benefits(participant_name=session['participant_name'], scheme=1, eligible=form.scheme1.data,
                                               received=form.scheme1_received.data,
                                               benefits=form.scheme1_benefits.data)
            scheme2_userdata = scheme_benefits(participant_name=session['participant_name'], scheme=2, eligible=form.scheme2.data,
                                               received=form.scheme1_received.data,
                                               benefits=form.scheme2_benefits.data)
            scheme3_userdata = scheme_benefits(participant_name=session['participant_name'], scheme=3, eligible=form.scheme3.data,
                                               received=form.scheme1_received.data,
                                               benefits=form.scheme3_benefits.data)
            scheme4_userdata = scheme_benefits(participant_name=session['participant_name'], scheme=4, eligible=form.scheme4.data,
                                               received=form.scheme1_received.data,
                                               benefits=form.scheme4_benefits.data)
            scheme5_userdata = scheme_benefits(participant_name=session['participant_name'], scheme=5, eligible=form.scheme5.data,
                                               received=form.scheme1_received.data,
                                               benefits=form.scheme5_benefits.data)
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
            # flash(f'user_talks {form.participant_name} added successfully', 'success')
            return render_template("admin.html")
        return render_template("addSchemes.html", form=form, legend="Schemes")
    return redirect(url_for('root'))

@app.route("/admin/product/<int:product_id>", methods=['GET'])
def product(product_id):
    if isUserAdmin():
        product = Product.query.get_or_404(product_id)
        return render_template('adminProduct.html', product=product)
    return redirect(url_for('root'))


@app.route("/admin/product/<int:product_id>/update", methods=['GET', 'POST'])
def update_product(product_id):
    if isUserAdmin():
        product = Product.query.get_or_404(product_id)
        form = addProductForm()
        form.category.choices = [(row.categoryid, row.category_name) for row in Category.query.all()]
        if form.validate_on_submit():
            if form.image.data:
                product.image = save_picture(form.image.data)
            product.product_name = form.productName.data
            product.sku = form.sku.data
            product.productDescription = form.productDescription.data
            product.stock = form.productQuantity.data
            # product.discounted_price = form.data.discounted_price = 15
            product.regular_price = form.productPrice.data
            db.session.commit()
            product_category = ProductCategory.query.filter_by(productid=product.productid).first()
            if form.category.data != product_category.categoryid:
                new_product_category = ProductCategory(categoryid=form.category.data, productid=product.productid)
                db.session.add(new_product_category)
                db.session.commit()
                db.session.delete(product_category)
                db.session.commit()

            flash('This product has been updated!', 'success')
            return redirect(url_for('getProducts'))
        elif request.method == 'GET':
            form.productName.data = product.product_name
            form.sku.data = product.sku
            form.productDescription.data = product.description
            form.productPrice.data = product.regular_price
            form.productQuantity.data = product.stock
        return render_template('addProduct.html', legend="Update Product", form=form)
    return redirect(url_for('root'))


@app.route("/admin/product/<int:product_id>/delete", methods=['POST'])
def delete_product(product_id):
    if isUserAdmin():
        product_category = ProductCategory.query.filter_by(productid=product_id).first()
        if product_category is not None:
            db.session.delete(product_category)
            db.session.commit()
        Cart.query.filter_by(productid=product_id).delete()
        db.session.commit()
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        flash('Your product has been deleted!', 'success')
    return redirect(url_for('getProducts'))


@app.route("/admin/users", methods=['GET'])
def getUsers():
    if isUserAdmin():
        # users = User.query.all()
        print('in')
        cur = mysql.connection.cursor()
        cur.execute(
            'SELECT u.fname, u.lname, u.email, u.active, u.city, u.state, COUNT(o.orderid) as noOfOrders FROM `user` u LEFT JOIN `order` o ON u.userid = o.userid GROUP BY u.userid')
        users = cur.fetchall()
        return render_template('adminUsers.html', users=users)
    return redirect(url_for('root'))


@app.route("/removeFromCart")
def removeFromCart():
    if isUserLoggedIn():
        productId = int(request.args.get('productId'))
        removeProductFromCart(productId)
        return redirect(url_for('cart'))
    else:
        return redirect(url_for('loginForm'))


@app.route("/checkoutPage")
def checkoutForm():
    if isUserLoggedIn():
        cartdetails, totalsum, tax = getusercartdetails()
        return render_template("checkoutPage.html", cartData=cartdetails, totalsum=totalsum, tax=tax)
    else:
        return redirect(url_for('loginForm'))


@app.route("/createOrder", methods=['GET', 'POST'])
def createOrder():
    loggedIn = getLoginUserDetails()
    totalsum = request.args.get('total')
    email, username, ordernumber, address, fullname, phonenumber, provider = extractOrderdetails(request, totalsum)
    if email:
        sendEmailconfirmation(email, username, ordernumber, phonenumber, provider)

    return render_template("OrderPage.html", email=email, username=username, ordernumber=ordernumber,
                           address=address, fullname=fullname, phonenumber=phonenumber, loggedIn=loggedIn)


@app.route("/orders", methods=['GET', 'POST'])
def orders():
    loggedIn, firstName, productCountinKartForGivenUser = getLoginUserDetails()
    return render_template('404.html', loggedIn=loggedIn, firstName=firstName)


@app.route("/profile", methods=['GET', 'POST'])
def profile():
    loggedIn, firstName, productCountinKartForGivenUser = getLoginUserDetails()
    return render_template('404.html', loggedIn=loggedIn, firstName=firstName)

@app.route("/forgotPassword", methods=['GET', 'POST'])
def forgotPassword():
    loggedIn, firstName, productCountinKartForGivenUser = getLoginUserDetails()
    return render_template('404.html', loggedIn=loggedIn, firstName=firstName)


@app.route("/seeTrends", methods=['GET', 'POST'])
def seeTrends():
    trendtype = str(request.args.get('trend'))
    cur = mysql.connection.cursor()
    if (trendtype == "least"):
        cur.execute("SELECT ordered_details.productid, sum(ordered_details.quantity) AS TotalQuantity,product.product_name FROM \
                       ordered_details,product where ordered_details.productid=product.productid GROUP BY productid \
                           ORDER BY TotalQuantity ASC LIMIT 3 ")
    else:
        trendtype = "most"
        cur.execute("SELECT ordered_details.productid, sum(ordered_details.quantity) AS TotalQuantity,product.product_name FROM \
                ordered_details,product where ordered_details.productid=product.productid GROUP BY productid \
                    ORDER BY TotalQuantity DESC LIMIT 3 ")

    products = cur.fetchall()
    cur.close()
    x = []
    y = []
    for item in products:
        x.append(item['product_name'])
        y.append(item['TotalQuantity'])

    my_plot_div = plot([go.Bar(x=x, y=y)], output_type='div')

    return render_template('trends.html',
                           div_placeholder=Markup(my_plot_div), trendtype=trendtype
                           )