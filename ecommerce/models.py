from datetime import datetime
from ecommerce import db

db.Model.metadata.reflect(db.engine)


class User(db.Model):
    __table_args__ = {'extend_existing': True}
    userid = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(100), unique=False, nullable=False)
    city = db.Column(db.String(100), unique=False, nullable=False)
    state = db.Column(db.String(100), unique=False, nullable=False)
    country = db.Column(db.String(100), unique=False, nullable=False)
    zipcode = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"User('{self.fname}', '{self.lname}'), '{self.password}', " \
               f"'{self.address}', '{self.city}', '{self.state}', '{self.country}'," \
               f"'{self.zipcode}','{self.email}','{self.phone}')"


class Category(db.Model):
    __table_args__ = {'extend_existing': True}
    categoryid = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Category('{self.categoryid}', '{self.category_name}')"


class Product(db.Model):

    __table_args__ = {'extend_existing': True}
    productid = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(50), nullable=False)
    product_name = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    image = db.Column(db.String(1000), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    regular_price = db.Column(db.DECIMAL)
    discounted_price = db.Column(db.DECIMAL)
    product_rating = db.Column(db.DECIMAL)
    product_review = db.Column(db.String(100), nullable=True)
    sub_product_id = db.Column(db.String(200), nullable=True)
    brand = db.Column(db.String(200), nullable=True)
    weight = db.Column(db.String(200), nullable=True)

class user_talks(db.Model):
    __table_args__ = {'extend_existing': True}
    survey_start_place = db.Column(db.String(50))
    name = db.Column(db.String(50))
    user_mobile_number = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    village_name = db.Column(db.String(100))
    caste = db.Column(db.String(1000))
    occupation = db.Column(db.String(100))
    supporting_party = db.Column(db.String(100))
    roads = db.Column(db.String(100))
    drinage = db.Column(db.String(100))
    grave_yards = db.Column(db.String(100))
    water = db.Column(db.String(100))
    houses = db.Column(db.String(100))
    land_allotments = db.Column(db.String(100))
    current_mla = db.Column(db.String(100))
    number_of_visits_current = db.Column(db.Integer)
    ex_mla = db.Column(db.String(100))
    number_of_visits_ex = db.Column(db.Integer)
    future_contestents = db.Column(db.String(200))
    expectations = db.Column(db.String(500))
    head_of_each_caste_name = db.Column(db.String(200))
    caste_head_mobile_number = db.Column(db.Integer)

    def __repr__(self):
        return f"Product('{self.productid}','{self.product_name}','{self.description}', '{self.image}',  '{self.stock}','{self.regular_price}', '{self.discounted_price}', '{self.sub_product_id}', '{self.brand}','{self.weight}')"

class scheme_benefits(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    participant_name = db.Column(db.String(100))
    scheme = db.Column(db.Integer)
    eligible = db.Column(db.String(3))
    received = db.Column(db.String(3))
    benefits = db.Column(db.String(1000))

    def __repr__(self):
        return f"Product('{self.participant_name}','{self.scheme}','{self.eligible}', '{self.received}',  '{self.benefits}')"

class ProductCategory(db.Model):
    __table_args__ = {'extend_existing': True}
    categoryid = db.Column(db.Integer, db.ForeignKey('category.categoryid'), nullable=False, primary_key=True)
    productid = db.Column(db.Integer, db.ForeignKey('product.productid'), nullable=False, primary_key=True)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Product('{self.categoryid}', '{self.productid}')"

class SubProducts(db.Model):
    __table_args__ = {'extend_existing': True}
    product_id = db.Column(db.Integer, nullable=False,  primary_key=True)
    sub_product_id = db.Column(db.Integer, nullable=False ,  primary_key=True)
    weights = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f"SubProduct('{self.product_id}', '{self.sub_product_id}', '{self.weights}')"

class Cart(db.Model):
    __table_args__ = {'extend_existing': True}
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False, primary_key=True)
    productid = db.Column(db.Integer, db.ForeignKey('product.productid'), nullable=False, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    subproductid = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"Cart('{self.userid}', '{self.productid}, '{self.quantity}', '{self.subproductid}')"


class Order(db.Model):
    __table_args__ = {'extend_existing': True}
    orderid = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, nullable=False)
    total_price = db.Column(db.DECIMAL, nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False, primary_key=True)

    def __repr__(self):
        return f"Order('{self.orderid}', '{self.order_date}','{self.total_price}','{self.userid}'')"
#
class OrderedProduct(db.Model):
    __tablename__ = "ordered_details"
    __table_args__ = {'extend_existing': True}
    ordproductid = db.Column(db.Integer, primary_key=True)
    orderid = db.Column(db.Integer,db.ForeignKey('order.orderid'), nullable=False)
    productid = db.Column(db.Integer,db.ForeignKey('product.productid'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    subproductid = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Order('{self.ordproductid}', '{self.orderid}','{self.productid}','{self.quantity}','{self.subproductid}')"



class SaleTransaction(db.Model):
    __table_args__ = {'extend_existing': True}
    transactionid = db.Column(db.Integer, primary_key=True)
    orderid = db.Column(db.Integer,db.ForeignKey('order.orderid'), nullable=False)
    transaction_date = db.Column(db.DateTime,nullable=False)
    amount = db.Column(db.DECIMAL, nullable=False)
    cc_number=db.Column(db.String(50), nullable=False)
    cc_type = db.Column(db.String(50), nullable=False)
    response = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Order('{self.transactionid}', '{self.orderid}','{self.transactiondate}','{self.amount}', '{self.cc_number}','{self.cc_type}','{self.response}')"