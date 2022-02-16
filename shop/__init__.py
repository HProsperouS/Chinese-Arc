from ast import keyword
import imp
import csv
from top_selling import Top_selling
from json import load
from email.policy import default
from itertools import count
from math import prod
from msilib import change_sequence
from operator import methodcaller
from re import split, sub, template
from venv import create
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_required
import shelve
from HomeAnnouncement import HomeAnnouncement
from FAQ import FAQ
from Feedback import Feedback
from cust_order import CustOrder
from Unsubscribe import Unsubscribe
from count import Count
from voucher import Voucher
from Subscriptions import Subscriptions
import functools
from Order_form import CreateCustOrder
from Newsletter import Newsletter
from Voucher_form import CreateVoucherForm
from EditHomeAnnouncement import CreateHomeAnnouncementForm, UpdateHomeAnnouncementForm
from EditProduct import UpdateProductForm, CreateProductForm, photos
from Contact import Contact
from ContactReply import ContactReply
from earnings import Revenue
from flask_uploads import configure_uploads,UploadSet,IMAGES
from Order_form import CreateCustOrder
from Forms import Registration, CreateSubscriptionsForm, CreateFAQForm, Register_AdminForm, Login_AdminForm, CreateNewsletterForm, UpdateAdminForm, CreateUnsubscribeForm, CreateContactForm, CreateContactReplyForm,CreateDeliveryFeedbackForm, CreateFeedbackForm,Registration,  CreateFAQForm, Login,CreateOrderForm, Registration, CreateFAQForm, CreateFeedbackForm
from DeliveryFeedback import DeliveryFeedback
from Voucher_form import CreateVoucherForm, UpdateVoucherForm
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import ProductInfo
from ProductInfo import ProductInfo
from email.message import EmailMessage
import Customer
import urllib.request
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from heapq import nlargest

# flask uploads
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SECRET_KEY'] = 'Chinese ARC'

app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images/')

app.config['UPLOAD_EXTENSIONS'] = ['.jpeg', '.jpg', '.png', '.gif']
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login_admin'
login_manager.login_message = 'Please login as admin'


class Admin(UserMixin):

    def __init__(self, username,email, gender,roles,status,create_date, password):
        self.id = 0
        self.username = username
        self.gender = gender
        self.email = email
        self.roles = roles
        self.status = status
        self.create_date = create_date
        self.password = password

    def set_id(self, id):
        self.id = id

    def set_username(self, username):
        self.username = username

    def set_gender(self, gender):
        self.gender = gender

    def set_email(self, email):
        self.email = email

    def set_roles(self, roles):
        self.roles = roles

    def set_status(self, status):
        self.status = status

    def set_create_date(self, create_date):
        self.create_date = create_date

    def set_password(self, password):
        self.password = password

    def get_id(self):
        return self.id

    def get_username(self):
        return self.username

    def get_gender(self):
        return self.gender

    def get_email(self):
        return self.email

    def get_roles(self):
        return self.roles

    def get_status(self):
        return self.status

    def get_create_date(self):
        return self.create_date

    def get_password(self):
        return self.password

    def __repr__(self):
        return f'<Admin: {self.username}>'

def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "login" not in session:
            return redirect(url_for("login_admin", next=request.url))
        return func(*args, **kwargs)

    return secure_function

@login_manager.user_loader
def user_loader(user_id):
    return Admin.get_id(user_id)

@app.route('/register_admin', methods=['POST', 'GET'])
def register_admin():
    register_admin_form = Register_AdminForm(request.form)    
    if request.method == 'POST' and register_admin_form.validate():
        try:
            admins_dict = {}
            db = shelve.open('Admin.db', 'r')
            admins_dict = db['Admin']
        except IOError:
            print("An Error occured when retrieving data from Admin.db")
        finally:
            db.close()

        admins_list = []
        
        for key in admins_dict:
            admin = admins_dict.get(key)
            if admin.email == register_admin_form.email.data:
                admins_list.append(admin)
        email = register_admin_form.email.data
        for admin in admins_list:
            print(admin.get_email())
            print(email)
            if email == admin.email:
                # if register_admin_form.email.data in admins_dict:
                flash('You have already registered with the existing email.', 'danger')
                return redirect(url_for('register_admin'))
            else:
                try:
                    admins_dict = {}
                    db = shelve.open('Admin.db', 'c')
                    admins_dict = db['Admin']
                except:
                    print("Error in retrieving Users from Admin.db.")
                hashed_password = generate_password_hash(register_admin_form.password.data, method='sha256')
                admin = Admin(
                            register_admin_form.username.data,
                            register_admin_form.email.data,
                            register_admin_form.gender.data,
                            register_admin_form.roles.data,
                            register_admin_form.status.data,
                            register_admin_form.create_date.data,
                            hashed_password
                            )
                if len(admins_dict) == 0:
                        currentid = 1
                else:
                    #  [-1] means the last element in a sequence
                    last = list(admins_dict.keys())[-1]
                    currentid = int(last + 1)
                admin.set_id(currentid)
                admins_dict[admin.get_id()] = admin
                db['Admin'] = admins_dict
                db.close()
                flash('Hi'+ " " + admin.get_username() +', You have successfully registered','success')
                return redirect(url_for('login_admin'))
    return render_template('register_admin.html', form=register_admin_form)

@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    login_admin_form = Login_AdminForm(request.form)
    if request.method == 'POST' and login_admin_form.validate():
        try:
            admins_dict = {}
            db = shelve.open('Admin.db', 'r')
            admins_dict = db['Admin']
        except IOError:
            print("An Error occured when retrieving data from Admin.db")
        finally:
            db.close()

        admins_list = []
        
        for id in admins_dict:
            admin = admins_dict.get(id)
            admins_list.append(admin)

        for admin in admins_list:
            # print(admin.get_email())
            # print(admin.get_password())
            if login_admin_form.email.data == admin.email:
                if admin.get_status() == 'Enabled':
                    password = login_admin_form.password.data
                    # print(password)
                    if check_password_hash(admin.password, password):
                        session['login'] = admin.id
                        session['loggedIn'] = admin.username
                        session['acctype'] = admin.roles
                        flash("Hi," + session.get('loggedIn') + ", "+"Welcome to Chinese Arc ",'success')
                        return redirect(url_for('dashboard',userid=session['login']))
                    else:
                        flash('Please enter correct account or password','danger')
                else:
                    flash("Hi, Your Account is disaled, Please Contact Chinese Arc for more information", 'info')

    return render_template('login_admin.html', form=login_admin_form)



@app.route('/logout_admin')
@login_required
def logout_admin():
    session.clear()
    return redirect(url_for('login_admin'))

@app.route('/logout_home')
@login_required
def logout_home():
    session.clear()
    return redirect(url_for('home_page'))
    
@app.route('/profile_admin')
@login_required
def profile_admin():
    try:
        admins_dict = {}
        db = shelve.open('Admin.db', 'r')
        admins_dict = db['Admin']
    except:
        print("An error occured when retrieving data from Admin.db")
    finally:
        db.close()

    admins_list = []
    for key in admins_dict:
        # To get current user
        if key == session.get('login'):
            admin = admins_dict.get(key)
            admins_list.append(admin)
        
    return render_template('ProfileAdmin.html', 
                            count1 = len(admins_list), 
                            admins_list=admins_list
                            )
    

@app.route('/DisableAdmin/<int:id>/', methods=['GET', 'POST'])
@login_required
def DisableAdmin(id):
    try:
        admins_dict = {}
        db = shelve.open('Admin.db', 'w')
        admins_dict = db['Admin']
    except IOError:
        print("An error occurred trying to read ProductInfo.db")

    admin = admins_dict.get(id)
    admin.set_status('Disabled')
    db['Admin'] = admins_dict
    db.close()
    flash('Hi'+ " "+', You have successfully Enabled ' + admin.get_username() + " ",'success')

    return redirect(url_for('RetrieveAdmin'))

@app.route('/EnableAdmin/<int:id>/', methods=['GET', 'POST'])
@login_required
def EnableAdmin(id):
    try:
        admins_dict = {}
        db = shelve.open('Admin.db', 'w')
        admins_dict = db['Admin']
    except IOError:
        print("An error occurred trying to read ProductInfo.db")

    admin = admins_dict.get(id)
    admin.set_status('Enabled')
    db['Admin'] = admins_dict
    db.close()
    flash('Hi'+ " "+', You have successfully enabled ' + admin.get_username() + " ",'success')
    return redirect(url_for('RetrieveAdmin'))

@app.route('/DeleteAdmin/<int:id>', methods=['POST'])
@login_required
def DeleteAdmin(id):
    try:
        admins_dict = {}
        db = shelve.open('Admin.db', 'w')
        admins_dict = db['Admin']
    except IOError:
        print("An error occurred trying to read Admin.db")
    admins_dict.pop(id)
    print(id)

    db['Admin'] = admins_dict
    db.close()

    return redirect(url_for('RetrieveAdmin'))


@app.route('/RetrieveAdmin')
@login_required
def RetrieveAdmin():
    try:
        admins_dict = {}
        db = shelve.open('Admin.db', 'r')
        admins_dict = db['Admin']
    except:
        print("An error occured when retrieving data from Admin.db")
    finally:
        db.close()

    admins_list = []
    for key in admins_dict:
        admin = admins_dict.get(key)
        admins_list.append(admin)
        
    return render_template('RetrieveAdmin.html', 
                            count1 = len(admins_list), 
                            admins_list=admins_list
                            )

@app.route('/EditAdminProfile/<int:id>/', methods=['GET', 'POST'])
@login_required
def EditAdminProfile(id):
    EditAdminProfile = UpdateAdminForm(request.form)
    if request.method == 'POST' and EditAdminProfile.validate():
        try:
            admins_dict = {}
            db = shelve.open('Admin.db', 'w')
            admins_dict = db['Admin']
        except IOError:
            print("An error occured when retrieving from Admin.db")

        hashed_password = generate_password_hash(EditAdminProfile.password.data, method='sha256')
        admin = admins_dict.get(id)
        admin.set_username(EditAdminProfile.username.data)
        admin.set_email(EditAdminProfile.email.data)
        admin.set_gender(EditAdminProfile.gender.data)
        admin.set_roles(EditAdminProfile.roles.data)
        # admin.set_create_date(EditAdminProfile.create_date.data)
        admin.set_password(hashed_password)
        db['Admin'] = admins_dict
        db.close() 
        flash("You have success updated your profile","info")
        return redirect(url_for('profile_admin'))
    else:
        try:
            admins_dict = {}
            db = shelve.open('Admin.db','r')
            admins_dict = db['Admin']
        except IOError:
            print("An error occured when retrieving from Admin.db")
        finally:
            db.close()

        admin = admins_dict.get(id)
        EditAdminProfile.username.data = admin.get_username()
        EditAdminProfile.email.data = admin.get_email()
        EditAdminProfile.gender.data = admin.get_gender()
        EditAdminProfile.roles.data = admin.get_roles()
        EditAdminProfile.create_date.data = admin.get_create_date()
        # EditAdminProfile.password.data = admin.get_password()


        return render_template('UpdateAdminProfile.html', form=EditAdminProfile)


@app.route('/register_page', methods=['POST', 'GET'])
def register_page():
    register = Registration(request.form)
    if request.method == 'POST' and register.validate():
        cust_dict = {}
        db = shelve.open('customer.db', 'c')
        try:
            cust_dict = db['customers']
        except:
            print("Error in retrieving Users from customer.db.")

        customer = Customer.Customer(
                                    register.first_name.data,
                                    register.last_name.data,
                                    register.email.data,
                                    register.gender.data,
                                    register.birthdate.data,
                                    register.city.data,
                                    register.postal_code.data,
                                    register.address.data,
                                    register.password.data
                                    )
        cust_dict[customer.get_customer_id()] = customer
        db['customers'] = cust_dict
        db.close()
        return redirect(url_for('login_page'))
    return render_template('register.html', form=register)



@app.route('/login_page', methods=['POST','GET'])
def login_page():

    customer = []

    login_page = Login(request.form)

    if request.method == 'POST' and login_page.validate():

        try:
            cust_dict = {}
            db = shelve.open('customer.db', 'r')
            cust_dict = db['customers']
        except:
            print('Error in retrieving Users from account.db.')

        finally:
            db.close()

        for key in cust_dict:
            customer_loggedin = cust_dict.get(key)
            print(key)
            print(customer_loggedin.get_email())
            print(customer_loggedin.get_password())
            if login_page.email.data == customer_loggedin.get_email() and login_page.password.data == customer_loggedin.get_password():
                session['true'] = True
                session['logged_in'] = customer_loggedin.get_first_name() + ' ' + customer_loggedin.get_last_name()
                session['user_id'] = key
                customer.append(customer_loggedin)

                flash('Hi'+ " " + customer_loggedin.get_first_name() + ' ' + customer_loggedin.get_last_name() + ", You have successfully logged in","success")
                return redirect(url_for('home_page'))

            else:
                print('Account or Password is wrong, Please try again.')
    return render_template('login.html', form=login_page)

@app.route('/update_profile_page')
def update_profile_page():
    try:
        cust_dict = {}
        db = shelve.open('customer.db', 'r')
        cust_dict = db['customers']
    except IOError:
        print('An error occurred trying to read')
    finally:
        db.close()

    cust_list = []
    for key in cust_dict:
        customer = cust_dict.get(key)
        cust_list.append(customer)
    
    try:
        cust_order_dict = {}
        db = shelve.open('CustOrder.db', 'r')
        cust_order_dict = db['CustOrder']
    except:
        print('Unable to read data')
    finally:
        db.close()

    cust_order_list = []
    for key in cust_order_dict:
        cust_order = cust_order_dict.get(key)
        cust_order_list.append(cust_order)

    return render_template('profile.html', count=len(cust_list),
                           cust_list=cust_list, count2=len(cust_order_list), cust_order_list=cust_order_list)
                           
@app.route('/update_customer_info/<int:id>', methods=['GET', 'POST'])
def update_cust_info(id):
    update_cust_form=Registration(request.form)
    if request.method == 'POST' and update_cust_form.validate():
        cust_dict = {}
        db = shelve.open('customer.db', 'w')
        cust_dict = db['customers']

        customer = cust_dict.get(id)
        customer.set_first_name(update_cust_form.first_name.data)
        customer.set_last_name(update_cust_form.last_name.data)
        customer.set_gender(update_cust_form.gender.data)
        customer.set_birthdate(update_cust_form.birthdate.data)
        customer.set_city(update_cust_form.city.data)
        customer.set_postal_code(update_cust_form.postal_code.data)
        customer.set_address(update_cust_form.address.data)
        customer.set_email(update_cust_form.email.data)
        customer.set_password(update_cust_form.password.data)

        db['customers'] = cust_dict
        db.close()

        flash('Profile has been updated successfully',"success")
        return redirect(url_for('update_profile_page'))
    else:
        cust_dict = {}
        db = shelve.open('customer.db', 'r')
        cust_dict = db['customers']
        db.close()

        customer = cust_dict.get(id)

        (update_cust_form.first_name.data) = customer.get_first_name()
        (update_cust_form.last_name.data) = customer.get_last_name()
        (update_cust_form.gender.data) = customer.get_gender()
        (update_cust_form.birthdate.data) = customer.get_birthdate()
        (update_cust_form.city.data) = customer.get_city()
        (update_cust_form.postal_code.data) = customer.get_postal_code()
        (update_cust_form.address.data) = customer.get_address()
        (update_cust_form.email.data) = customer.get_email()
        (update_cust_form.password.data) = customer.get_password()

        return render_template('updateprofile.html', form=update_cust_form)


@app.route('/logout_page')
def logout_page():
    session.clear()
    return redirect(url_for('home_page'))


@app.route('/')
@app.route('/home')
def home_page():
    try:
        productinfo_dict = {}
        db = shelve.open('ProductInfo.db', 'r')
        productinfo_dict = db['ProductInfo']
    except IOError:
        print('An error occurred trying to read from HomeAnnouncement.db')
    else:
        db.close()
    
    productinfo_list = []
    for key in productinfo_dict:
        productinfo = productinfo_dict.get(key)
        if productinfo.get_product_category() == 'Featured':
            productinfo_list.append(productinfo)

    image_list = os.listdir(app.config['UPLOADED_PHOTOS_DEST'])


    try:
        homeannouncement_dict = {}
        db = shelve.open('HomeAnnouncement.db', 'r')
        homeannouncement_dict = db['HomeAnnouncement']
    except IOError:
        print('An error occurred trying to read from HomeAnnouncement.db')
    finally:
        db.close()

    homeannouncement_list = []
    for key in homeannouncement_dict:
        homeannouncement = homeannouncement_dict.get(key)
        homeannouncement_list.append(homeannouncement)

    try:
        feedback_dict = {}
        db = shelve.open('Feedback.db', 'r')
        feedback_dict = db['Feedback']
    except IOError:
        print('An error occurred trying to read from Feedback.db')
    finally:
        db.close()

    feedback_list = []
    for key in feedback_dict:
        feedback = feedback_dict.get(key)
        feedback_list.append(feedback)

    return render_template('cust_home.html', 
                            count1=len(homeannouncement_list),
                            count2=len(image_list),
                            count3=len(productinfo_list),
                            homeannouncement_list=homeannouncement_list,
                            productinfo_list = productinfo_list,
                            image_list = image_list,
                            count=len(feedback_list),
                            feedback_list=feedback_list
                            )



# Create Error Pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Internal Server Error
@app.errorhandler(500)
def error500(e):
    return render_template('500.html'), 500


# Internal Server Error
@app.errorhandler(403)
def error403(e):
    return render_template('403.html'), 403

@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413



@app.route('/cust_women')
def women_product_page():
    try:
        productinfo_dict = {}
        db = shelve.open('ProductInfo.db', 'r')
        productinfo_dict = db['ProductInfo']
    except IOError:
        print('An error occurred trying to read from HomeAnnouncement.db')
    else:
        db.close()
    
    productinfo_list = []
    for key in productinfo_dict:
        productinfo = productinfo_dict.get(key)
        if productinfo.get_product_category() == 'Cheongsam':
            productinfo_list.append(productinfo)

    image_list = os.listdir(app.config['UPLOADED_PHOTOS_DEST'])

    return render_template('cust_women.html',
                            count1=len(image_list),
                            count2=len(productinfo_list),
                            productinfo_list = productinfo_list,
                            image_list = image_list,
                            )


@app.route('/cust_men')
def men_product_page():
    try:
        productinfo_dict = {}
        db = shelve.open('ProductInfo.db', 'r')
        productinfo_dict = db['ProductInfo']
    except IOError:
        print('An error occurred trying to read from HomeAnnouncement.db')
    else:
        db.close()
    
    productinfo_list = []
    for key in productinfo_dict:
        productinfo = productinfo_dict.get(key)
        if productinfo.get_product_category() == 'TangZhuang':
            productinfo_list.append(productinfo)

    image_list = os.listdir(app.config['UPLOADED_PHOTOS_DEST'])

    return render_template('cust_men.html',
                            count1=len(image_list),
                            count2=len(productinfo_list),
                            productinfo_list = productinfo_list,
                            image_list = image_list,
                            )


@app.route('/cust_accessories')
def accessories_page():
    try:
        productinfo_dict = {}
        db = shelve.open('ProductInfo.db', 'r')
        productinfo_dict = db['ProductInfo']
    except IOError:
        print('An error occurred trying to read from HomeAnnouncement.db')
    else:
        db.close()
    
    productinfo_list = []
    for key in productinfo_dict:
        productinfo = productinfo_dict.get(key)
        if productinfo.get_product_category() == 'Accessories':
            productinfo_list.append(productinfo)

    image_list = os.listdir(app.config['UPLOADED_PHOTOS_DEST'])

    return render_template('cust_accessory.html',
                            count1=len(image_list),
                            count2=len(productinfo_list),
                            productinfo_list = productinfo_list,
                            image_list = image_list,
                            )



@app.route('/about_us')
def about_us_page():
    return render_template('aboutUs.html')



@app.route('/forgot_password')
def forgot_password_page():
    return render_template('forgot_password.html')



@app.route('/dashboard')
@login_required
def dashboard():
    
    try:
        top_selling_dict = {}
        db = shelve.open('Top_selling.db','r')
        top_selling_dict = db['Top_selling']
    except:
        print("Error in retrieving data from Feedback.db.")
    finally:
        db.close()

    top_selling_list = []
    for key in top_selling_dict:
        top = top_selling_dict.get(key)
        top_selling_list.append(top)
        print(top_selling_list)
    
    def getTopselling(top_selling_list):
        return nlargest(3, top_selling_list, key = lambda product:product.getQuantity())

    top = getTopselling(top_selling_list)
    top_selling_dict_2 = {}

    top_selling_list_2 = []
    top_selling_list_3 = []
    sum = 0
    qty = 0
    for x in top_selling_dict:
        total = top_selling_dict.get(x)
        sum += total.getPrice()
    for y in top_selling_dict:
        total = top_selling_dict.get(y)
        qty += total.getQuantity()
    top_selling_list_2.append(sum)
    top_selling_list_3.append(qty)
    print(top_selling_list_2)
    

     
    for i in top:
        top_selling_dict_2[i.getName()] = i.getQuantity()
        print(i.getName(),':',i.getQuantity())

    try:
        cust_order_dict = {}
        db = shelve.open('CustOrder.db', 'r')
        cust_order_dict = db['CustOrder']
    except:
        print('Unable to read data')
    finally:
        db.close()

    cust_order_list = []
    for key in cust_order_dict:
        cust_order = cust_order_dict.get(key)
        cust_order_list.append(cust_order)
    
    try:
        delete_order_dict = {}
        db = shelve.open('deleteorder.db', 'r')
        delete_order_dict = db['deleteOrder']
    except:
        print('Error in opening db')
    finally:
        db.close()

    delete_order_list = []
    for key in delete_order_dict:
        delete_order = delete_order_dict.get(key)
        delete_order_list.append(delete_order)

    try:
        product_dict = {}
        db = shelve.open('ProductInfo.db', 'r')
        product_dict = db['ProductInfo']
    except IOError:
        print('An error occurered trying to read PRODUCTINFO.db')
    finally:
        db.close()

     # product list of Featured
    product_list = []
    for key in product_dict:
        product = product_dict.get(key)
        product_list.append(product)


    try:
        admins_dict = {}
        db = shelve.open('Admin.db', 'r')
        admins_dict = db['Admin']
    except:
        print("An error occured when retrieving data from Admin.db")
    finally:
        db.close()

    admins_list = []
    for key in admins_dict:
        admin = admins_dict.get(key)
        admins_list.append(admin)

    try:
      earnings_dict = {}
      db = shelve.open('Earnings.db', 'r')
      earnings_dict = db['Earnings']
    except:
        print('error in retrieving revenue.ab')
    finally:
        db.close

    revenue_list = []
    for key in earnings_dict:
        earnings = earnings_dict.get(key)
        revenue_list.append(earnings)
        
    return render_template('dashboard.html', 
                            count=len(cust_order_list),
                            count1 = len(admins_list),
                            count2 = len(delete_order_list),
                            count3 = len(product_list),
                            count4 = len(revenue_list),
                            cust_order_list=cust_order_list,
                            admins_list=admins_list,
                            delete_order_list=delete_order_list,
                            product_list=product_list,
                            revenue_list=revenue_list,
                            top_selling_dict_2=top_selling_dict_2,
                            top_selling_list_2=top_selling_list_2,
                            top_selling_list_3=top_selling_list_3
                            )



@app.route('/chart')
@login_required
def chart():
    return render_template('chart.html')




@app.route('/voucher')
@login_required
def voucher():
    try:
        voucher_dict = {}
        db = shelve.open('voucher.db', 'r')
        voucher_dict = db['Vouchers']
    except(IOError):
        print('Unable to read data')
    finally:
        db.close()
    voucher_list = []
    for key in voucher_dict:
        order = voucher_dict.get(key)
        voucher_list.append(order)

    return render_template('Voucher.html', count=len(voucher_list), voucher_list=voucher_list)


@app.route('/voucherform', methods=['GET', 'POST'])
@login_required
def voucherform():
   create_voucher_form = CreateVoucherForm(request.form)
   if request.method == 'POST' and create_voucher_form.validate():
        voucher_dict = {}
        db = shelve.open('voucher.db', 'c')

        try:
            voucher_dict = db['Vouchers']
        except:
            print("Error in retrieving Users from order.db.")

        voucher = Voucher(create_voucher_form.name.data,
                        create_voucher_form.desc.data,
                        create_voucher_form.type.data,
                        create_voucher_form.secret.data,
                        create_voucher_form.code.data, 
                            
                        create_voucher_form.total.data,
                        create_voucher_form.status.data, 
                        create_voucher_form.date.data,
                        create_voucher_form.end_date.data,
                        create_voucher_form.create_date.data,
                        create_voucher_form.create_by.data,
                        create_voucher_form.mod_date.data,
                        create_voucher_form.mod_by.data)
        voucher_dict[voucher.get_voucher_id()] = voucher
        db['Vouchers'] = voucher_dict
        return redirect(url_for('voucher'))
   return render_template('Voucher_form.html', form=create_voucher_form)
@app.route('/updatevoucher/<int:id>', methods=['GET', 'POST'])
@login_required
def update_voucher(id):
    update_voucher_form=UpdateVoucherForm(request.form)
    if request.method == 'POST' and update_voucher_form.validate():
        voucher_dict = {}
        db = shelve.open('voucher.db', 'w')
        voucher_dict = db['Vouchers']

        voucher = voucher_dict.get(id)
        voucher.set_name(update_voucher_form.name.data)
        voucher.set_desc(update_voucher_form.desc.data)
        voucher.set_type(update_voucher_form.type.data)
        voucher.set_secret(update_voucher_form.secret.data)
        voucher.set_code(update_voucher_form.code.data)
        voucher.set_total(update_voucher_form.total.data)
        voucher.set_status(update_voucher_form.status.data)
        
        voucher.set_date(update_voucher_form.date.data)
        voucher.set_end_date(update_voucher_form.end_date.data)

        voucher.set_create_date(update_voucher_form.create_date.data)
        voucher.set_create_by(update_voucher_form.create_by.data)
        voucher.set_modified_date(update_voucher_form.mod_date.data)
        voucher.set_modified_by(update_voucher_form.mod_by.data)

        db['Vouchers'] = voucher_dict
        db.close()
        flash('Voucher has been updated sucessfully')
        return redirect(url_for('voucher'))
    else:
        voucher_dict = {}
        db = shelve.open('voucher.db', 'r')
        voucher_dict = db['Vouchers']
        db.close()

        voucher = voucher_dict.get(id)

        update_voucher_form.name.data = voucher.get_voucher_name()
        update_voucher_form.desc.data = voucher.get_voucher_desc()
        update_voucher_form.secret.data = voucher.get_voucher_secret()
        (update_voucher_form.code.data) = voucher.get_voucher_code()
        update_voucher_form.total.data = voucher.get_voucher_total()
        update_voucher_form.status.data = voucher.get_voucher_status()
        update_voucher_form.date.data = voucher.get_voucher_date()
        update_voucher_form.type.data = voucher.get_voucher_type()
        update_voucher_form.end_date.data = voucher.get_voucher_end_date()

        update_voucher_form.create_date.data = voucher.get_create_date()
        update_voucher_form.create_by.data = voucher.get_create_by()

        update_voucher_form.mod_by.data = voucher.get_modified_by()



        return render_template('Update_Voucher_form.html', form=update_voucher_form)


@app.route('/deletevoucher/<int:id>', methods=['POST'])
@login_required
def delete_voucher(id):
    voucher_dict = {}
    db = shelve.open('voucher.db', 'w')
    voucher_dict = db['Vouchers']

    voucher_dict.pop(id)

    db['Vouchers'] = voucher_dict
    db.close()
    flash('Voucher has been deleted sucessfully')
    return redirect(url_for('voucher'))



@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')


@app.route('/catalog')
@login_required
def catalog():
    try:
        product_dict = {}
        db = shelve.open('ProductInfo.db', 'r')
        product_dict = db['ProductInfo']
    except IOError:
        print('An error occurered trying to read PRODUCTINFO.db')
    finally:
        db.close()

     # product list of Featured
    product_list = []
    for key in product_dict:
        product = product_dict.get(key)
        product_list.append(product)

    # product list of Featured
    product_list1 = []
    for key in product_dict:
        product = product_dict.get(key)
        if product.get_product_category() == 'Featured': 
            product_list1.append(product)

    # product list of Cheongsam
    product_list2 = []
    for key in product_dict:
        product = product_dict.get(key)
        if product.get_product_category() == 'Cheongsam': 
            product_list2.append(product)

    # product list of TangZhuang
    product_list3 = []
    for key in product_dict:
        product = product_dict.get(key)
        if product.get_product_category() == 'TangZhuang': 
            product_list3.append(product)

    # product list of  # product list of Featured
    product_list4 = []
    for key in product_dict:
        product = product_dict.get(key)
        if product.get_product_category() == 'Accessories': 
            product_list4.append(product)

    product_list6 = []
    for key in product_dict:
        product = product_dict.get(key)
        if product.get_status() == 'Low Stock' or product.get_status() == 'Out Of Stock' : 
            product_list6.append(product)

    image_list = os.listdir(app.config['UPLOADED_PHOTOS_DEST'])

    return render_template('Catalog.html', 
                            count=len(product_list),
                            count1=len(product_list1),
                            count2=len(product_list2),
                            count3=len(product_list3),
                            count4=len(product_list4),
                            count6=len(product_list6), 
                            count5=len(image_list),
                            image_list=image_list, 
                            product_list=product_list,
                            product_list1=product_list1,
                            product_list2=product_list2,
                            product_list3=product_list3,
                            product_list4=product_list4,
                            product_list6=product_list6,
                            )

@app.route('/CreateProduct', methods=['GET', 'POST'])
@login_required
def CreateProduct():
    # WTForms provides a FileField to render a file type input.
    # It doesn't do anything special with the uploaded data.
    # However, since Flask splits the form data (request.form) and the file data (request.files)
    # You need to make sure to pass the correct data when creating the form.
    # You can use a CombinedMultiDict to combine the two into a single structure that WTForms understands.
    CreateProduct_Form = CreateProductForm(CombinedMultiDict((request.files, request.form)))
    if request.method == 'POST' and CreateProduct_Form.validate():
        # Pass it a filename and it will return a secure version of it. 
        # This filename can then safely be stored on a regular file system and passed to os.path.join(). 
        # The filename returned is an ASCII only string for maximum portability.
        filename = secure_filename(CreateProduct_Form.product_image.data.filename)
        # if the filename not blank
        if filename != '':
           # os.path.splitext() method in Python is used to split the path name into a pair root and ext.
           # In this case, it is use to get file ext, like png, txt, pptx, docx etc
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                return "Invalid Image", 400
            else:
                productinfo_dict = {}
                db = shelve.open('ProductInfo.db', 'c')

                try:
                    productinfo_dict = db['ProductInfo']
                except:
                    print("Error in retrieving products from database")

                productinfo = ProductInfo(
                    filename,
                    CreateProduct_Form.product_name.data,
                    CreateProduct_Form.product_category.data,
                    CreateProduct_Form.product_price.data,
                    CreateProduct_Form.product_description.data,
                    CreateProduct_Form.product_stock.data,
                    CreateProduct_Form.create_date.data,
                    CreateProduct_Form.create_by.data,
                    CreateProduct_Form.modified_date.data,
                    CreateProduct_Form.modified_by.data,

                )
                if len(productinfo_dict) == 0:
                    currentproductid = 1
                else:
                    #  [-1] means the last element in a sequence
                    last = list(productinfo_dict.keys())[-1]
                    currentproductid = last + 1
                productinfo.set_product_id(currentproductid)

                productinfo_dict[productinfo.get_product_id()] = productinfo
                db['ProductInfo'] = productinfo_dict

                # The images uploaded will put it to static/images
                if CreateProduct_Form.product_category.data == 'Cheongsam':
                    CreateProduct_Form.product_image.data.save(os.path.join(basedir, 'static/images/Cheongsam', filename))
                elif CreateProduct_Form.product_category.data == 'TangZhuang':
                    CreateProduct_Form.product_image.data.save(os.path.join(basedir, 'static/images/TangZhuang', filename))
                elif CreateProduct_Form.product_category.data == 'Accessories':
                    CreateProduct_Form.product_image.data.save(os.path.join(basedir, 'static/images/Accessories', filename))
                else:
                    CreateProduct_Form.product_image.data.save(os.path.join(basedir, 'static/images/Featured', filename))

                flash('Product has created sucessfully','success')
                print(productinfo.get_product_id())
                return redirect(url_for('catalog', filename=filename))
    return render_template('CreateProduct.html', form=CreateProduct_Form)



@app.route('/UpdateProduct/<int:id>', methods=['GET', 'POST'])
@login_required
def update_product(id):
    UpdateProduct_Form = UpdateProductForm(CombinedMultiDict((request.files, request.form)))
    if request.method == 'POST' and UpdateProduct_Form.validate():
        filename = secure_filename(UpdateProduct_Form.product_image.data.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                return "Invalid Image", 400
            else:
                if UpdateProduct_Form.product_category.data == 'Cheongsam':
                    UpdateProduct_Form.product_image.data.save(os.path.join(basedir, 'static/images/Cheongsam', filename))
                elif UpdateProduct_Form.product_category.data == 'TangZhaung':
                    UpdateProduct_Form.product_image.data.save(os.path.join(basedir, 'static/images/TangZhuang', filename))
                elif UpdateProduct_Form.product_category.data == 'Accessories':
                    UpdateProduct_Form.product_image.data.save(os.path.join(basedir, 'static/images/Accessories', filename))
                else:
                    UpdateProduct_Form.product_image.data.save(os.path.join(basedir, 'static/images/Featured', filename))

                productinfo_dict = {}
                db = shelve.open('ProductInfo.db', 'w')
                productinfo_dict = db['ProductInfo']

                productinfo = productinfo_dict.get(id)
                productinfo.set_product_image(filename)
                productinfo.set_product_name(UpdateProduct_Form.product_name.data)
                productinfo.set_product_category(UpdateProduct_Form.product_category.data)
                productinfo.set_product_price(UpdateProduct_Form.product_price.data)
                productinfo.set_product_description(UpdateProduct_Form.product_description.data)
                productinfo.set_product_stock(UpdateProduct_Form.product_stock.data)
                productinfo.set_create_date(UpdateProduct_Form.create_date.data)
                productinfo.set_create_by(UpdateProduct_Form.create_by.data)
                productinfo.set_modified_date(UpdateProduct_Form.modified_date.data)
                productinfo.set_modified_by(UpdateProduct_Form.modified_by.data)
                db['ProductInfo'] = productinfo_dict
                db.close()
                flash('Product has updated sucessfully','success')
                return redirect(url_for('catalog'))

    else:
        try:
            productinfo_dict = {}
            db = shelve.open('ProductInfo.db', 'r')
            productinfo_dict = db['ProductInfo']
        except IOError:
            print('An error occurred trying to read ProductInfo.db')
        finally:
            db.close()

        productinfo = productinfo_dict.get(id)
        UpdateProduct_Form.product_image.data = productinfo.get_product_image()
        UpdateProduct_Form.product_name.data = productinfo.get_product_name()
        UpdateProduct_Form.product_category.data = productinfo.get_product_category()
        UpdateProduct_Form.product_price.data = productinfo.get_product_price()
        UpdateProduct_Form.product_description.data = productinfo.get_product_description()
        UpdateProduct_Form.product_stock.data = productinfo.get_product_stock()
        UpdateProduct_Form.create_date.data = productinfo.get_create_date()
        UpdateProduct_Form.create_by.data = productinfo.get_create_by()
        # UpdateProduct_Form.modified_date.data = productinfo.get_modified_date()
        UpdateProduct_Form.modified_by.data = productinfo.get_modified_by()

        return render_template('UpdateProduct.html', form=UpdateProduct_Form)



@app.route('/DeleteProduct/<int:id>', methods=['POST'])
@login_required
def delete_product(id):
    try:
        product_dict = {}
        db = shelve.open('ProductInfo.db', 'w')
        product_dict = db['ProductInfo']
    except IOError:
        print("An error occurred trying to read ProductInfo.db")
    product_dict.pop(id)
    print(id)
    db['ProductInfo'] = product_dict
    flash('Product has deleted sucessfully','info')
    db.close()

    return redirect(url_for('catalog'))



@app.route('/Announcement')
@login_required
def Announcement():
    try:
        homeannouncement_dict = {}
        db = shelve.open('HomeAnnouncement.db', 'r')
        homeannouncement_dict = db['HomeAnnouncement']
    except IOError:
        print('An error occurred trying to read')
    finally:
        db.close()

    homeannouncement_list = []
    for key in homeannouncement_dict:
        homeannouncement = homeannouncement_dict.get(key)
        homeannouncement_list.append(homeannouncement)

    return render_template('Announcement.html', count=len(homeannouncement_list),
                           homeannouncement_list=homeannouncement_list)



#TO COMMEND OUT CREATEANNOUNCEMENT IS BECAUSE I ONLY WANT THE DATABASE TO STORE 1 ANNOUNCEMENT, AND ONLY ALLOW ADMIN TO UPDATE IT.

@app.route('/CreateAnnouncement',methods=['GET','POST'])
@login_required
def CreateAnnouncement():
    CreateHomeAnnouncement_Form=CreateHomeAnnouncementForm(request.form)
    if request.method == 'POST' and CreateHomeAnnouncement_Form.validate():
        homeannouncement_dict = {}
        db = shelve.open('HomeAnnouncement.db', 'c')

        try:
            homeannouncement_dict = db['HomeAnnouncement']
        except:
            print("Error in retrieving data from HomeAnnouncement.db.")

        homeannouncement = HomeAnnouncement(CreateHomeAnnouncement_Form.title.data, 
                                            CreateHomeAnnouncement_Form.text.data, 
                                            CreateHomeAnnouncement_Form.create_date.data,
                                            CreateHomeAnnouncement_Form.create_by.data, 
                                            CreateHomeAnnouncement_Form.modified_date.data, 
                                            CreateHomeAnnouncement_Form.modified_by.data
                                            )
        homeannouncement_dict[homeannouncement.get_id()] = homeannouncement
        db['HomeAnnouncement'] = homeannouncement_dict
        return redirect(url_for('Announcement'))
    return render_template('CreateHomeAnnouncement.html', form=CreateHomeAnnouncement_Form)

@app.route('/UpdateHomeAnnouncemnet/<int:id>/', methods=['GET', 'POST'])
@login_required
def UpdateHomeAnnouncement(id):
    UpdateHomeAnnouncement_Form = UpdateHomeAnnouncementForm(request.form)

    if request.method == 'POST' and UpdateHomeAnnouncement_Form.validate():
        try:
            homeannouncement_dict = {}
            db = shelve.open('HomeAnnouncement.db', 'w')
            homeannouncement_dict = db['HomeAnnouncement']
        except IOError:
            print("An Error occured when retrieve from HomeAnnouncement.db")

        homeannouncement = homeannouncement_dict.get(id)
        homeannouncement.set_title(UpdateHomeAnnouncement_Form.title.data)
        homeannouncement.set_text(UpdateHomeAnnouncement_Form.text.data)
        homeannouncement.set_create_date(UpdateHomeAnnouncement_Form.create_date.data)
        homeannouncement.set_create_by(UpdateHomeAnnouncement_Form.create_by.data)
        homeannouncement.set_modified_date(UpdateHomeAnnouncement_Form.modified_date.data)
        homeannouncement.set_modified_by(UpdateHomeAnnouncement_Form.modified_by.data)
        db['HomeAnnouncement'] = homeannouncement_dict
        db.close()

        return redirect(url_for('Announcement'))

    else:
        try:
            homeannouncement_dict = {}
            db = shelve.open('HomeAnnouncement.db', 'r')
            homeannouncement_dict = db['HomeAnnouncement']
        except IOError:
            print('An error occurred trying to read HomeAnnouncement.db')
        finally:
            db.close()

        homeannouncement = homeannouncement_dict.get(id)
        UpdateHomeAnnouncement_Form.title.data = homeannouncement.get_title()
        UpdateHomeAnnouncement_Form.text.data = homeannouncement.get_text()
        UpdateHomeAnnouncement_Form.create_date.data = homeannouncement.get_create_date()
        UpdateHomeAnnouncement_Form.create_by.data = homeannouncement.get_create_by()
        # UpdateHomeAnnouncement_Form.modified_date.data = homeannouncement.get_modified_date()
        UpdateHomeAnnouncement_Form.modified_by.data = homeannouncement.get_modified_by()
        return render_template('UpdateHomeAnnouncement.html', form=UpdateHomeAnnouncement_Form)

@app.route('/FAQ')
@login_required
def FAQs():
    try:
        faq_dict = {}
        db = shelve.open('FAQ.db', 'r')
        faq_dict = db['FAQ']
    except IOError:
        print('An error occurred trying to read FAQ database')
    finally:
        db.close()

    faq_list = []
    for key in faq_dict:
        faq = faq_dict.get(key)
        faq_list.append(faq)
    # print( faq_list)
    return render_template('FAQ_admin.html', count=len(faq_list),
                           faq_list=faq_list)

@app.route('/UpdateFaqs/<uuid:id>/', methods=['GET', 'POST'])
@login_required
def update_FAQs(id):
    UpdateFAQ_Form = CreateFAQForm(request.form)

    if request.method == 'POST' and UpdateFAQ_Form.validate():

        faq_dict = {}
        db = shelve.open('FAQ.db', 'w')
        faq_dict = db['FAQ']

        faq = faq_dict.get(id)
        faq.set_question(UpdateFAQ_Form.question.data)
        faq.set_answer(UpdateFAQ_Form.answer.data)
        faq.set_create_date(UpdateFAQ_Form.create_date.data)
        db['FAQ'] = faq_dict
        db.close()

        return redirect(url_for('FAQs'))

    else:
        try:
            faq_dict = {}
            db = shelve.open('FAQ.db', 'r')
            faq_dict = db['FAQ']
        except IOError:
            print('An error occurred trying to read FAQ.db')
        finally:
            db.close()

        faq = faq_dict.get(id)
        UpdateFAQ_Form.question.data = faq.get_question()
        UpdateFAQ_Form.answer.data = faq.get_answer()
        UpdateFAQ_Form.create_date.data = faq.get_create_date()

        return render_template('UpdateFAQs.html', form=UpdateFAQ_Form)

@app.route('/CreateFAQ',methods=['GET','POST'])
@login_required
def CreateFAQ():
    CreateFAQ_Form=CreateFAQForm(request.form)
    if request.method == 'POST' and CreateFAQ_Form.validate():
        faq_dict = {}
        db = shelve.open('FAQ.db', 'c')

        try:
            faq_dict = db['FAQ']
        except:
            print("Error in retrieving data from FAQ.db.")

        faq = FAQ(CreateFAQ_Form.question.data, CreateFAQ_Form.answer.data, CreateFAQ_Form.create_date.data)
        faq_dict[faq.get_id()] = faq
        db['FAQ'] = faq_dict
        flash('New FAQ uploaded sucessfully','success')
        return redirect(url_for('FAQs'))
    return render_template('CreateFAQ.html', form=CreateFAQ_Form)

@app.route('/DeleteFAQ/<uuid:id>', methods=['POST'])
@login_required
def delete_FAQs(id):
    faq_dict = {}
    db = shelve.open('FAQ.db', 'w')
    faq_dict = db['FAQ']

    faq_dict.pop(id)
    print(id)

    db['FAQ'] = faq_dict
    db.close()

    return redirect(url_for('FAQs'))

@app.route('/FAQ_CUST')
def FAQs_cust():
    try:
        faq_dict = {}
        db = shelve.open('FAQ.db', 'r')
        faq_dict = db['FAQ']
    except IOError:
        print('An error occurred trying to read FAQ database')
    finally:
        db.close()

    faq_list = []
    for key in faq_dict:
        faq = faq_dict.get(key)
        faq_list.append(faq)

    return render_template('FAQs_cust.html', count=len(faq_list),
                           faq_list=faq_list)

@app.route('/CreateDeliveryFeedback',methods=['GET','POST'])
def CreateDeliveryFeedback():
    CreateDeliveryFeedback_Form=CreateDeliveryFeedbackForm(request.form)
    if request.method == 'POST' and CreateDeliveryFeedback_Form.validate():
        deliveryfeedback_dict = {}
        db = shelve.open('DeliveryFeedback.db', 'c')

        try:
           deliveryfeedback_dict = db['DeliveryFeedback']
        except:
            print("Error in retrieving data from DeliveryFeedback.db.")
        #deliveryfeedback
        deliveryfeedback = DeliveryFeedback(CreateDeliveryFeedback_Form.email_address.data,
                                            CreateDeliveryFeedback_Form.product.data,
                                            CreateDeliveryFeedback_Form.rating.data,
                                            CreateDeliveryFeedback_Form.message1.data,
                                            CreateDeliveryFeedback_Form.message2.data,
                                            CreateDeliveryFeedback_Form.message3.data,
                                            CreateDeliveryFeedback_Form.message4.data,
                                            CreateDeliveryFeedback_Form.remarks.data,
                                            CreateDeliveryFeedback_Form.create_date.data,
                                            )
        if len(deliveryfeedback_dict) == 0:
                    currentid = 1
        else:
            #  [-1] means the last element in a sequence
            last = list(deliveryfeedback_dict.keys())[-1]
            currentid = last + 1
        deliveryfeedback.set_id(currentid)
        deliveryfeedback_dict[deliveryfeedback.get_id()] = deliveryfeedback
        db['DeliveryFeedback'] = deliveryfeedback_dict
        flash('Delivery Feeback sent sucessfully, Thank You for your','success')
        return redirect(url_for('home_page'))
    return render_template('CreateDeliveryFeedback.html', form=CreateDeliveryFeedback_Form)

@app.route('/DeleteDeliveryFeedback/<int:id>', methods=['POST'])
@login_required
def delete_deliveryfeedback(id):
    try:
        deliveryfeedback_dict = {}
        db = shelve.open('DeliveryFeedback.db', 'w')
        deliveryfeedback_dict = db['DeliveryFeedback']
        
    except IOError:
        print("Cannot open DeliveryFeedback.db")
    deliveryfeedback_dict.pop(id)
    print(id)

    db['DeliveryFeedback'] = deliveryfeedback_dict
    db.close()

    return redirect(url_for('RetrieveDeliveryFeedback'))

@app.route('/RetrieveDeliveryFeedback',methods=['GET','POST'])
@login_required
def RetrieveDeliveryFeedback():
    try:
        deliveryfeedback_dict = {}
        db = shelve.open('DeliveryFeedback.db', 'r')
        deliveryfeedback_dict = db['DeliveryFeedback']
    except IOError:
        print('An error occurred trying to read from DeliveryFeedback.db')
    finally:
        db.close()

    deliveryfeedback_list = []
    for key in deliveryfeedback_dict:
        deliveryfeedback = deliveryfeedback_dict.get(key)
        deliveryfeedback_list.append(deliveryfeedback)

    return render_template('RetrieveDeliveryFeedback.html', count=len(deliveryfeedback_list),
                        deliveryfeedback_list=deliveryfeedback_list)

#Subscription Function: Create
@app.route('/createSubscriptions', methods=['GET', 'POST'])
def create_subscriptions():
    create_subscriptions_form = CreateSubscriptionsForm(request.form)
    if request.method == 'POST' and create_subscriptions_form.validate():
        subscriptions_dict = {}
        db = shelve.open('subscriptions.db', 'c')

        try:
            subscriptions_dict = db['Subscriptions']

        except:
            print("Error in retrieving Subscriptions from subscriptions.db.")

        subscriptions = Subscriptions(create_subscriptions_form.first_name.data, 
                                        create_subscriptions_form.last_name.data, 
                                        create_subscriptions_form.email.data)
        subscriptions_dict[subscriptions.get_subscriptions_id()] = subscriptions
        db['Subscriptions'] = subscriptions_dict

        create_subscriptions_form.email.data = subscriptions.get_email()
        subscriptions_id = subscriptions.get_subscriptions_id()
        sender_email = "testingusers1236@gmail.com"
        receiver_email = subscriptions.get_email()
        password = "dG09#G.@Yg23G"

        message = MIMEMultipart("alternative")
        message["Subject"] = 'Newsletter Subscription' + ' ( Subscription ID: ' + str(subscriptions_id) + ' ) '
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create the plain-text and HTML version of your message
        text = """\
        Hi,
        Welcome To The Chinese Arc Family!
        """
        html = """\
        <html>
        <body bgcolor="#E1E1E1" leftmargin="0" marginwidth="0" topmargin="0" marginheight="0" offset="0">
        <center style="background-color:#E1E1E1;">
        <table border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" id="bodyTbl" style="table-layout: fixed;max-width:100% !important;width: 100% !important;min-width: 100% !important;">
            <tr>
            <td align="center" valign="top" id="bodyCell">

                <table bgcolor="#E1E1E1" border="0" cellpadding="0" cellspacing="0" width="500" id="emailHeader">
                <tr>
                    <td align="center" valign="top">

                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                        <td align="center" valign="top">

                            <table border="0" cellpadding="10" cellspacing="0" width="500" class="flexibleContainer">
                            <tr>
                                <td valign="top" width="500" class="flexibleContainerCell">

                                <table align="left" border="0" cellpadding="0" cellspacing="0" width="100%">
                                    <tr>
                                    <td align="left" valign="middle" id="invisibleIntroduction" class="flexibleContainerBox" style="display:none;display:none !important;">
                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:100%;">
                                        <tr>
                                            <td align="left" class="textContent">
                                            <div style="font-family:Helvetica,Arial,sans-serif;font-size:13px;color:#828282;text-align:center;line-height:120%;">
                                                Here you can put short introduction of your email template.
                                            </div>
                                            </td>
                                        </tr>
                                        </table>
                                    </td>
                                    <td align="right" valign="middle" class="flexibleContainerBox">
                                    </td>
                                    </tr>
                                </table>
                                </td>
                            </tr>
                            </table>

                        </td>
                        </tr>
                    </table>

                    </td>
                </tr>
                </table>

                <table bgcolor="#FFFFFF" border="0" cellpadding="0" cellspacing="0" width="500" id="emailBody">

                <tr>
                    <td align="center" valign="top">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="color:#FFFFFF;" bgcolor="#3498db">
                        <tr>
                        <td align="center" valign="top">
                            <table border="0" cellpadding="0" cellspacing="0" width="500" class="flexibleContainer">
                            <tr>
                                <td align="center" valign="top" width="500" class="flexibleContainerCell">
                                <table border="0" cellpadding="30" cellspacing="0" width="100%">
                                    <tr>
                                    <td align="center" valign="top" class="textContent">
                                        <h1 style="color:#FFFFFF;line-height:100%;font-family:Helvetica,Arial,sans-serif;font-size:35px;font-weight:normal;margin-bottom:5px;text-align:center;">Welcome To The Chinese Arc Family!</h1>
                                        <h2 style="text-align:center;font-weight:normal;font-family:Helvetica,Arial,sans-serif;font-size:23px;margin-bottom:10px;color:#205478;line-height:135%;">     </h2>
                                        <div style="text-align:center;font-family:Helvetica,Arial,sans-serif;font-size:15px;margin-bottom:0;color:#FFFFFF;line-height:135%;">Thanks for subscribing to our newsletter! <br><br> You will receive newsletters regarding exclusvie store-wide sales and many more! </div>
                                    </td>
                                    </tr>
                                </table>
                                </td>
                            </tr>
                            </table>
                        </td>
                        </tr>
                    </table>
                    </td>
                </tr>

                <tr>
                    <td align="center" valign="top">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                        <td align="center" valign="top">
                            <table border="0" cellpadding="0" cellspacing="0" width="500" class="flexibleContainer">
                            <tr>
                                <td align="center" valign="top" width="500" class="flexibleContainerCell">

                                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                    <tr>
                                    <td valign="top" class="imageContent">
                                        <img src="https://c.tenor.com/Rdz9M0h2BoQAAAAC/confetti.gif" width="500" class="flexibleImage" style="max-width:500px;width:100%;display:block;" alt="Text" title="Text" />
                                    </td>
                                    </tr>
                                </table>

                                </td>
                            </tr>
                            </table>
                        </td>
                        </tr>
                    </table>
                    </td>
                </tr>

                <tr>
                    <td align="center" valign="top">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                        <td align="center" valign="top">
                            <table border="0" cellpadding="0" cellspacing="0" width="500" class="flexibleContainer">
                            <tr>
                                <td align="center" valign="top" width="500" class="flexibleContainerCell">
                                <table border="0" cellpadding="30" cellspacing="0" width="100%">
                                    <tr>
                                    <td align="center" valign="top">

                                        <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                        <tr>
                                            <td valign="top" class="textContent">
                                            <h3 style="color:#5F5F5F;line-height:125%;font-family:Helvetica,Arial,sans-serif;font-size:20px;font-weight:normal;margin-top:0;margin-bottom:3px;text-align:left;">Style Tip Of The Day</h3>
                                            <div style="text-align:left;font-family:Helvetica,Arial,sans-serif;font-size:15px;margin-bottom:0;margin-top:3px;color:#5F5F5F;line-height:135%;">Create a moodboard to develop your personal style. Remember that personal style is an experiment; you never know what amazing looks await you until you're in the dressing room. Take time to play with colors and shapes to find what looks great on your unique body.</div>
                                            </td>
                                        </tr>
                                        </table>

                                    </td>
                                    </tr>
                                </table>
                                </td>
                            </tr>
                            </table>
                        </td>
                        </tr>
                    </table>
                    </td>
                </tr>
            

                </table>

                <!-- footer -->
                <table bgcolor="#E1E1E1" border="0" cellpadding="0" cellspacing="0" width="500" id="emailFooter">
                <tr>
                    <td align="center" valign="top">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                        <td align="center" valign="top">
                            <table border="0" cellpadding="0" cellspacing="0" width="500" class="flexibleContainer">
                            <tr>
                                <td align="center" valign="top" width="500" class="flexibleContainerCell">
                                <table border="0" cellpadding="30" cellspacing="0" width="100%">
                                    <tr>
                                    <td valign="top" bgcolor="#E1E1E1">

                                        <div style="font-family:Helvetica,Arial,sans-serif;font-size:13px;color:#828282;text-align:center;line-height:120%;">
                                        <div>Copyright &#169; 2022. All rights reserved.</div>
                                        <div>If you don't want to receive these emails from us in the future, please <a href="http://127.0.0.1:5000/createUnsubscribe" target="_blank" style="text-decoration:none;color:#828282;"><span style="color:#828282;">Unsubscribe</span></a></div>
                                        </div>

                                    </td>
                                    </tr>
                                </table>
                                </td>
                            </tr>
                            </table>
                        </td>
                        </tr>
                    </table>
                    </td>
                </tr>
                </table>
                <!-- // end of footer -->

            </td>
            </tr>
        </table>
        </center>
        </body>
        </html>
        """

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )

        db.close()

        flash("You have successfully subscribed to TCA Newsletter", "success")

        return redirect(url_for('home_page'))
    return render_template('createSubscriptions.html', form=create_subscriptions_form)

# Subscription function: retrieve subscription + unsubscription
@app.route('/retrieveSubscriptions')
@login_required
def retrieve_subscriptions():
    try:
        subscriptions_dict = {}
        db = shelve.open('subscriptions.db', 'r')
        subscriptions_dict = db['Subscriptions']

        unsubscribe_dict = {}
        db = shelve.open('unsubscribe.db', 'r')
        unsubscribe_dict = db['Unsubscribe']

    except IOError:
        print('An error occurred trying to read DB')

    finally:
        db.close()

    subscriptions_list = []
    for key in subscriptions_dict:
        subscriptions = subscriptions_dict.get(key)
        subscriptions_list.append(subscriptions)

    unsubscribe_list = []
    for key in unsubscribe_dict:
        unsubscribe = unsubscribe_dict.get(key)
        unsubscribe_list.append(unsubscribe)

    #counting average rating for subscription:
    rating_list = []
    for key in unsubscribe_dict:
        unsubscribe = unsubscribe_dict.get(key)
        rating = unsubscribe.get_rating()
        rating_list.append(int(rating))

    #counting of each reason:
    irrelevant_list = []
    for key in unsubscribe_dict:
        irrelevant = unsubscribe_dict.get(key)
        if irrelevant.get_reason() == 'Irrelevant Content':
            irrelevant_list.append(irrelevant)

    many_list = []
    for key in unsubscribe_dict:
        many = unsubscribe_dict.get(key)
        if many.get_reason() == 'Too many emails':
            many_list.append(many)

    preferences_list = []
    for key in unsubscribe_dict:
        preferences = unsubscribe_dict.get(key)
        if preferences.get_reason() == 'Not tailored to my preferences':
            preferences_list.append(preferences)

    return render_template('retrieveSubscriptions.html', 
                            count=len(subscriptions_list), 
                            subscriptions_list=subscriptions_list,
                            count1=len(unsubscribe_list), 
                            unsubscribe_list=unsubscribe_list,
                            count2=len(irrelevant_list), 
                            irrelevant_list=irrelevant_list,
                            count3=len(many_list), 
                            many_list=many_list,
                            count4=len(preferences_list), 
                            preferences_list=preferences_list,
                            count5=len(rating_list),
                            sum1 = sum(rating_list), 
                            rating_list=rating_list
                            )

# Unsubscribe function: create
@app.route('/createUnsubscribe', methods=['GET', 'POST'])
def create_unsubscribe():
    create_unsubscribe_form = CreateUnsubscribeForm(request.form)
    if request.method == 'POST' and create_unsubscribe_form.validate():
        unsubscribe_dict = {}
        db = shelve.open('unsubscribe.db', 'c')

        try:
            unsubscribe_dict = db['Unsubscribe']
        except:
            print("Error in retrieving Unsubscribe from unsubscribe.db.")

        unsubscribe = Unsubscribe(create_unsubscribe_form.sub_id.data,
                                    create_unsubscribe_form.email.data,
                                    create_unsubscribe_form.rating.data, 
                                    create_unsubscribe_form.reason.data,
                                    create_unsubscribe_form.explaination.data)

        unsubscribe_dict[unsubscribe.get_unsubscribe_id()] = unsubscribe
        db['Unsubscribe'] = unsubscribe_dict

        #getting the sub_id input from unsubscribe:
        create_unsubscribe_form.sub_id.data = unsubscribe.get_sub_id()

        #checking with the subscriptions_dict:
        try:
            subscriptions_dict = {}
            db = shelve.open('subscriptions.db', 'r')
            subscriptions_dict = db['Subscriptions']

        except:
            print('An error occurred trying to read DB')

        finally:
            db.close()

        subscriptions_list = []
        for key in subscriptions_dict:
            subscriptions = subscriptions_dict.get(key)
            sub_uuid = subscriptions.get_subscriptions_id()
            subscriptions_list.append(sub_uuid)

        # removing those who requested to be unsubscribed:
        for i in subscriptions_list:
            if unsubscribe.get_sub_id() == str(i):
                subscriptions_dict = {}
                db = shelve.open('subscriptions.db', 'w')
                subscriptions_dict = db['Subscriptions']

                id = subscriptions.get_subscriptions_id()
                subscriptions_dict.pop(id)

                db['Subscriptions'] = subscriptions_dict
                db.close()

        db.close()

        return redirect(url_for('home_page'))
    return render_template('createUnsubscribe.html', form=create_unsubscribe_form)

# Newsletter function: create
@app.route('/createNewsletter', methods=['GET', 'POST'])
@login_required
def create_newsletter():
    create_newsletter_form = CreateNewsletterForm(request.form)
    if request.method == 'POST' and create_newsletter_form.validate():
        newsletter_dict = {}
        db = shelve.open('newsletter.db', 'c')

        try:
            newsletter_dict = db['Newsletter']
        except:
            print("Error in retrieving Newsletter from newsletter.db.")

        newsletter = Newsletter(create_newsletter_form.newsletter_name.data,
                                            create_newsletter_form.message.data,
                                            create_newsletter_form.create_date.data,
                                            create_newsletter_form.create_by.data,
                                            )

        newsletter_dict[newsletter.get_newsletter_id()] = newsletter
        db['Newsletter'] = newsletter_dict

        db.close()

        flash("Newsletter has been added successfully")

        return redirect(url_for('retrieve_newsletter'))
    return render_template('createNewsletter.html', form=create_newsletter_form)

# Newsletter function: retrieve
@app.route('/retrieveNewsletter')
@login_required
def retrieve_newsletter():
    try:
        newsletter_dict = {}
        db = shelve.open('newsletter.db', 'r')
        newsletter_dict = db['Newsletter']

        subscriptions_dict = {}
        db = shelve.open('subscriptions.db', 'r')
        subscriptions_dict = db['Subscriptions']

    except:
        print('An error occurred trying to read DB')

    finally:
        db.close()

    newsletter_list = []
    for key in newsletter_dict:
        newsletter = newsletter_dict.get(key)
        newsletter_list.append(newsletter)

    subscriptions_list = []
    for key in subscriptions_dict:
        subscriptions = subscriptions_dict.get(key)
        email = subscriptions.get_email()
        subscriptions_list.append(email)

    return render_template('retrieveNewsletter.html', count=len(newsletter_list), newsletter_list=newsletter_list)

# Newsletter function: update
@app.route('/updateNewsletter/<uuid:id>/', methods=['GET', 'POST'])
@login_required
def update_newslette(id):
    update_newsletter_form = CreateNewsletterForm(request.form)
    if request.method == 'POST' and update_newsletter_form.validate():

        try:
            newsletter_dict = {}
            db = shelve.open('newsletter.db', 'w')
            newsletter_dict = db['Newsletter']

            newsletter = newsletter_dict.get(id)
            newsletter.set_newsletter_name(update_newsletter_form.newsletter_name.data)
            newsletter.set_message(update_newsletter_form.message.data)
            newsletter.set_create_date(update_newsletter_form.create_date.data)
            newsletter.set_create_by(update_newsletter_form.create_by.data)

            db['Newsletter'] = newsletter_dict

        except:
            print('An error occurred trying to read newsletter.db')

        finally:
            db.close()
        
        return redirect(url_for('retrieve_newsletter'))

    else:
        try:
            newsletter_dict = {}
            db = shelve.open('newsletter.db', 'r')
            newsletter_dict = db['Newsletter']
            
        except:
            print('An error occurred trying to read newsletter.db')

        finally:
            db.close()

        flash("Newsletter have been updated")

        newsletter = newsletter_dict.get(id)
        update_newsletter_form.newsletter_name.data = newsletter.get_newsletter_name()
        update_newsletter_form.message.data = newsletter.get_message()
        update_newsletter_form.create_date.data = newsletter.get_create_date()
        update_newsletter_form.create_by.data = newsletter.get_create_by()
        
        return render_template('updateNewsletter.html', form=update_newsletter_form)

# Newsletter function: delete
@app.route('/deleteNewsletter/<uuid:id>', methods=['POST'])
@login_required
def delete_newsletter(id):
    try:
        newsletter_dict = {}
        db = shelve.open('newsletter.db', 'w')
        newsletter_dict = db['Newsletter']
        newsletter_dict.pop(id)
        db['Newsletter'] = newsletter_dict

    except:
        print('An error occurred trying to read DB')

    finally:
        db.close()

    flash("Newsletter have been deleted")

    return redirect(url_for('retrieve_newsletter'))

# Newsletter function: send newsletter to subscribers
@app.route('/sendNewsletter/<uuid:id>')
@login_required
def send_newsletter(id):
    create_newsletter_form = CreateNewsletterForm(request.form)

    newsletter_dict = {}
    db = shelve.open('newsletter.db', 'w')
    newsletter_dict = db['Newsletter']

    newsletter = newsletter_dict.get(id)
    create_newsletter_form.message.data = newsletter.get_message()
    create_newsletter_form.newsletter_name.data = newsletter.get_newsletter_name()

    subscriptions_dict = {}
    db = shelve.open('subscriptions.db', 'r')
    subscriptions_dict = db['Subscriptions']
    db.close()

    subscriptions_list = []
    for key in subscriptions_dict:
        subscriptions = subscriptions_dict.get(key)
        email = subscriptions.get_email()
        subscriptions_list.append(email)

    
    for i in subscriptions_list:
        sender_email = "testingusers1236@gmail.com"
        receiver_email = i
        password = "dG09#G.@Yg23G"

        message = MIMEMultipart("alternative")
        message["Subject"] = newsletter.get_newsletter_name()
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create the plain-text and HTML version of your message
        text = """\
        
        """
        html = """\
        <html>
        <body>
        </body>
        </html>
        """

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        part3 = MIMEText(newsletter.get_message(), "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)
        message.attach(part3)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )

    return render_template('sendNewsletter.html')

# #brings to customer account page
# @app.route('/base_cust')
# def base_cust():

#     return render_template('base_cust.html')

# @app.route('/dashboard_cust')
# def dashboard_cust():
#     return render_template('dashboard_cust.html')

# Product Feedback function: create
@app.route('/CreateFeedback',methods=['GET','POST'])
def CreateFeedback():
    CreateFeedback_Form = CreateFeedbackForm(request.form)
    if request.method == 'POST' and CreateFeedback_Form.validate():
        feedback_dict = {}
        db = shelve.open('Feedback.db', 'c')

        try:
           feedback_dict = db['Feedback']
        except:
            print("Error in retrieving data from Feedback.db.")

        feedback = Feedback(CreateFeedback_Form.product_name.data,
                                            CreateFeedback_Form.title.data,
                                            CreateFeedback_Form.rating.data,
                                            CreateFeedback_Form.fit.data,
                                            CreateFeedback_Form.quality.data,
                                            CreateFeedback_Form.description.data,
                                            CreateFeedback_Form.create_by.data,
                                            CreateFeedback_Form.create_date.data,
                                            )
        feedback_dict[feedback.get_feedback_id()] = feedback
        db['Feedback'] = feedback_dict

        flash('Your feedback has been sent sucessfully', 'success')

        return redirect(url_for('cust_order_history'))
    return render_template('CreateFeedback.html', form=CreateFeedback_Form)

# Product Feedback function: retrieve
@app.route('/RetrieveFeedback',methods=['GET','POST'])
def RetrieveFeedback():
    try:
        feedback_dict = {}
        db = shelve.open('Feedback.db', 'r')
        feedback_dict = db['Feedback']
    except IOError:
        print('An error occurred trying to read from Feedback.db')
    finally:
        db.close()

    feedback_list = []
    for key in feedback_dict:
        feedback = feedback_dict.get(key)
        feedback_list.append(feedback)

    return render_template('RetrieveFeedback.html', count=len(feedback_list),feedback_list=feedback_list)

# Product Feedback function: update
@app.route('/updateFeedback/<uuid:id>/', methods=['GET', 'POST'])
def UpdateFeedback(id):
    UpdateFeedback_Form = CreateFeedbackForm(request.form)
    if request.method == 'POST' and UpdateFeedback_Form.validate():

        try:
            feedback_dict = {}
            db = shelve.open('Feedback.db', 'w')
            feedback_dict = db['Feedback']

            feedback = feedback_dict.get(id)
            feedback.set_product_name(UpdateFeedback_Form.product_name.data)
            feedback.set_title(UpdateFeedback_Form.title.data)
            feedback.set_rating(UpdateFeedback_Form.rating.data)
            feedback.set_fit(UpdateFeedback_Form.fit.data)
            feedback.set_quality(UpdateFeedback_Form.quality.data)
            feedback.set_description(UpdateFeedback_Form.description.data)
            feedback.set_create_by(UpdateFeedback_Form.create_by.data)
            feedback.set_create_date(UpdateFeedback_Form.create_date.data)

            db['Feedback'] = feedback_dict

        except:
            print('An error occurred trying to read feedback.db')

        finally:
            db.close()

        flash("Feedback has been updated successfully")
        
        return redirect(url_for('RetrieveFeedback'))

    else:
        try:
            feedback_dict = {}
            db = shelve.open('Feedback.db', 'r')
            feedback_dict = db['Feedback']
            
        except:
            print('An error occurred trying to read feedback.db')

        finally:
            db.close()

        feedback = feedback_dict.get(id)
        UpdateFeedback_Form.product_name.data = feedback.get_product_name()
        UpdateFeedback_Form.title.data = feedback.get_title()
        UpdateFeedback_Form.rating.data = feedback.get_rating()
        UpdateFeedback_Form.fit.data = feedback.get_rating()
        UpdateFeedback_Form.quality.data = feedback.get_rating()
        UpdateFeedback_Form.description.data = feedback.get_rating()
        UpdateFeedback_Form.create_by.data = feedback.get_create_by()
        UpdateFeedback_Form.create_date.data = feedback.get_create_date()
        
        return render_template('updateFeedback.html', form=UpdateFeedback_Form)

# Product Feedback function: delete
@app.route('/deleteFeedback/<uuid:id>', methods=['POST'])
def DeleteFeedback(id):
    try:
        feedback_dict = {}
        db = shelve.open('Feedback.db', 'w')
        feedback_dict = db['Feedback']

        feedback_dict.pop(id)

        db['Feedback'] = feedback_dict
        flash('Feedback have been removed successfully')

    except:
        print('An error occurred trying to open Feedback.db')

    finally:
        db.close()

    return redirect(url_for('RetrieveFeedback'))

class Top_selling:
    def __init__(self, name, quantity,price):
        self.name = name
        self.quantity = quantity
        self.price = price
    def getName(self):
        return self.name
    def getQuantity(self):
        return self.quantity
    def getPrice(self):
        return self.price
    def setName(self,name):
        self.name = name
    def setQuantity(self, quantity):
        self.quantity = quantity
    def setPrice(self, price):
        self.price = price

    def getTopSelling(productList):
        top = nlargest(3, productList, key= lambda product:product.getQuantity())

@app.route('/createCustOrder', methods = ['GET', 'POST'])
def createCustOrder():
    try:
        cust_dict = {}
        db = shelve.open('customer.db', 'r')
        cust_dict = db['customers']
    except IOError:
        print('An error occurred trying to read')
    finally:
        db.close()

    cust_list = []
    for key in cust_dict:
        customer = cust_dict.get(key)
        cust_list.append(customer)
    
    
  

    try:  
        req = request.get_json()
        name = req['product_name']
        price = req['product_price']
        qty = req['product_qty']
        delete_add = req['function']
        print(req)
        try:
            product_dict = {}
            db = shelve.open('ProductInfo.db', 'r')
            product_dict = db['ProductInfo']
        except IOError:
            print('An error occurered trying to read PRODUCTINFO.db')
        finally:
            db.close()

        try:
            cust_cart_dict = {}
            db = shelve.open('custCart.db', 'w')
            cust_cart_dict = db['custCart']
        except:
            print('Error in opening db')

        for key in product_dict:
            product = product_dict.get(key)
            cust_cart_dict[0] = {'cart':1,'name':'cart','qty':0}
            if product.get_product_name() == name:          
                if delete_add == 'add':
                    count=Count()
                    cust_cart_dict[count.get_count()] = {'name':name,'price':price,'qty': qty}
                    print('created')
                elif delete_add == 'plus':
                    for key in list(cust_cart_dict):                   
                        if product.get_product_stock() >= cust_cart_dict[key]['qty']:
                            if cust_cart_dict[key]['name'] == name:
                                cust_cart_dict[key]['qty'] += 1
                                cust_cart_dict[key]['price'] += price
                                print('added')
                        if product.get_product_stock() < cust_cart_dict[key]['qty']:
                            cust_cart_dict[key]['qty'] -= 1
                            
                            print('Out of stock') 
                                    
                elif delete_add == 'minus':
                    for key in list(cust_cart_dict):
                        if cust_cart_dict[key]['name'] == name:
                            cust_cart_dict[key]['qty'] -= 1
                            cust_cart_dict[key]['price'] -= price
                            print('minus')
                            if cust_cart_dict[key]['qty'] == 0:
                                del cust_cart_dict[key]
                                print('item is 0 ( deleted )')
                elif delete_add == 'delete':
                    for key in list(cust_cart_dict):
                        if name == cust_cart_dict[key]['name']:
                            del cust_cart_dict[key]
                            print('removed')        
                
                    
        print(cust_cart_dict)
                
        db['custCart'] = cust_cart_dict
        db.close()
    except:
        print('error in receiving add to cart')

    if "true" not in session:
        flash("Please login as customer first","info")
        return redirect(url_for("login_page"))
    else:
        cust_cart_dict = {}
        db = shelve.open('custCart.db', 'c')
        try:
            cust_cart_dict = db['custCart']
        except :
            print("Error in retrieving cust Orders from CustCart.db.")
        db['custCart'] = cust_cart_dict
        db.close()

        create_custorder_form = CreateCustOrder(request.form)
        if request.method == 'POST' and create_custorder_form.validate():
            
            try:
                cust_cart_dict = {}
                db = shelve.open('custCart.db', 'r')
                cust_cart_dict = db['custCart']
            except:
                print('Error in opening cart db')
            finally:
                db.close()

            
            productinfo_dict = {}
            db = shelve.open('ProductInfo.db', 'w')
            productinfo_dict = db['ProductInfo']

            for key in productinfo_dict:
                product = productinfo_dict.get(key)
                for key in list(cust_cart_dict):                   
                    if product.get_product_name() == cust_cart_dict[key]['name']:
                        try:
                            top_selling_dict = {}
                            db = shelve.open('Top_selling.db', 'r')
                            top_selling_dict = db['Top_selling']
                        except:
                            print('error in top db')
                        finally:
                            db.close()
                        
                        if product.get_product_name() in top_selling_dict:
                            print('write')
                            try:
                                top_selling_dict = {}
                                db = shelve.open('Top_selling.db', 'w')
                                top_selling_dict = db['Top_selling']
                                top_selling_id = top_selling_dict.get(product.get_product_name())
                                qty = int(top_selling_id.getQuantity() + cust_cart_dict[key]['qty'])
                                price = int(top_selling_id.getPrice() +  cust_cart_dict[key]['price'])
                                top_selling_id.setQuantity(qty)
                                top_selling_id.setPrice(price)
                                print(top_selling_id.getQuantity())
                                print(top_selling_id.getPrice())
                               
                            except:
                                print('error in top db')
                            
                            db['Top_selling'] = top_selling_dict
                            db.close()

                            print(top_selling_dict)
                        elif product.get_product_name() not in top_selling_dict:
                            print('create')
                            try:
                                top_selling_dict = {}
                                db = shelve.open('Top_selling.db', 'c')
                                top_selling_dict = db['Top_selling']
                                top_selling = Top_selling(product.get_product_name(),cust_cart_dict[key]['qty'],cust_cart_dict[key]['price'])
                                top_selling_dict[product.get_product_name()] = top_selling
                                
                            except:
                                print('error in top db')


                            db['Top_selling'] = top_selling_dict
                            db.close()
                            

                            print(top_selling_dict)

                        

                       

                        
                        
                        
                        


                        stock = cust_cart_dict[key]['qty']
                        remain = product.get_product_stock() - stock
                        product.set_product_stock(remain)
                        print(remain)
                        with open('shop/static/data/Total.csv','r') as csv_file:
                            l=[]
                            csv_reader = csv.reader(csv_file)
                            Found = False
                            for line in csv_reader:
                                if line[0] == cust_cart_dict[key]['name']:
                                    Found=True
                                    line[1] = str(cust_cart_dict[key]['price'] + int(line[1]))
                                l.append(line)
                        csv_file.close()

                        if Found == False:
                            print('student not found')
                        else:
                            with open('shop/static/data/Total.csv','w+',newline='') as csv_file_2:
                                writer = csv.writer(csv_file_2)
                                writer.writerows(l)
                                csv_file_2.seek(0)
                                reader = csv.reader(csv_file_2)
                                for row in reader:
                                    print(row)
                                csv_file_2.close()

            try:
                db['ProductInfo'] =  productinfo_dict 
            except:
                print('error in opening product.db')
            finally:
                db.close()
            
            cust_order_dict = {}
            db = shelve.open('CustOrder.db', 'c')

            copy_cart_dict = cust_cart_dict.copy()

            try:
                cust_order_dict = db['CustOrder']
            except :
                print("Error in retrieving cust Orders from CustOrder.db.")

            Cust_orders = CustOrder(create_custorder_form.first_name.data,
                                    create_custorder_form.last_name.data,
                                    create_custorder_form.email.data,
                                    create_custorder_form.holder_name.data,
                                    create_custorder_form.card_type.data,
                                    create_custorder_form.card_num.data,
                                    create_custorder_form.cvv.data,
                                    create_custorder_form.city.data,
                                    create_custorder_form.postal_code.data,
                                    create_custorder_form.unit_number.data,
                                    create_custorder_form.create_date.data,
                                    create_custorder_form.modified_date.data,
                                    create_custorder_form.modified_by.data,
                                    create_custorder_form.status.data,
                                    create_custorder_form.total.data,
                                    create_custorder_form.discount.data)
            
            cust_order_dict[Cust_orders.get_custOrder_id()] = {'order':Cust_orders,'cart':copy_cart_dict} 

            db['CustOrder'] = cust_order_dict
            db.close()

            
            try:
                cust_cart_dict = {}
                db = shelve.open('custCart.db', 'w')
                cust_cart_dict = db['custCart']

                print(cust_cart_dict)

                cust_cart_dict.clear()

                cust_cart_dict[Cust_orders.get_custOrder_id()] = {'order':Cust_orders,'cart':copy_cart_dict} 
            except:
                print('Error in opening db')

                
            db['custCart'] = cust_cart_dict
            db.close()

           
            print(copy_cart_dict)

            # Refund
            refund_order_dict = {}
            db = shelve.open('refundorder.db', 'c')
            try:
                refund_order_dict = db['refundeOrder']
            except:
                print('Error in opening db')

            db['refundOrder'] = refund_order_dict 
            db.close()

            # Delete
            delete_order_dict = {}
            db = shelve.open('deleteorder.db', 'c')
            try:
                delete_order_dict = db['deleteOrder']
            except:
                print('Error in opening db')

            db['deleteOrder'] = delete_order_dict 
            db.close()

            # Delivered
            delivered_order_dict = {}
            db = shelve.open('deliveredorder.db', 'c')
            try:
                delivered_order_dict = db['deliveredOrder']
            except:
                print('Error in opening db')
            
            db['deliveredOrder'] = delivered_order_dict
            db.close()

            #  Earnings
            earnings_dict = {}
            db = shelve.open('Earnings.db', 'c')

            try:
                earnings_dict = db['Earnings']
            except :
                print("Error in retrieving cust Orders from CustOrder.db.")
        
            db['Earnings'] = earnings_dict
            db.close()

            flash("Order has been processed successfully! Thank you for shopping with Chinese Arc","info")
            return redirect(url_for('order_confirm'))
    
    return render_template('Customer_order_form.html', form=create_custorder_form,count=len(cust_list),
                                cust_list=cust_list)

@app.route('/order', methods=['GET','POST'])
@login_required
def retrieve_cust_orders():
    try:
        cust_cart_dict = {}
        db = shelve.open('custCart.db', 'w')
        cust_cart_dict = db['custCart']

        del cust_cart_dict[0]
    except:
        print('Error in opening db')


    try:
        cust_order_dict = {}
        db = shelve.open('CustOrder.db', 'r')
        cust_order_dict = db['CustOrder']
    except:
        print('Unable to read data')
    finally:
        db.close()

    cust_order_list = []
    for key in cust_order_dict:
        cust_order = cust_order_dict.get(key)
        cust_order_list.append(cust_order)

    cust_cart_dict = {}
    db = shelve.open('custCart.db', 'r')
    try:
        cust_cart_dict = db['custCart']
    except :
        print("Error in retrieving cust Orders from CustCart.db.")
    
    db.close()

    cust_cart_list = []
    for key in cust_cart_dict:
        cust_order = cust_cart_dict.get(key)
        cust_cart_list.append(cust_order)

    
    try:
        delete_order_dict = {}
        db = shelve.open('deleteorder.db', 'r')
        delete_order_dict = db['deleteOrder']
    except:
        print('Error in opening db')
    finally:
        db.close()

    delete_order_list = []
    for key in delete_order_dict:
        delete_order = delete_order_dict.get(key)
        delete_order_list.append(delete_order)

    
   
    return render_template('order.html', count=len(cust_order_list), cust_order_list=cust_order_list,count3=len(cust_cart_list),cust_cart_list=cust_cart_list,count4=len(delete_order_list),delete_order_list=delete_order_list)


@app.route('/deleteOrder/<uuid:id>', methods=['POST'])
@login_required
def delete_order(id):
    try:
        cust_order_dict = {}
        db = shelve.open('CustOrder.db', 'w')
        cust_order_dict = db['CustOrder']

        deleted_order_id = cust_order_dict.get(id)
        cust_order_dict.pop(id)

        db['CustOrder'] = cust_order_dict
        flash('Order has been deleted sucessfully')
    except:
        print('An error occured when opening CustOrder.db')
    finally:
        db.close()
    

    try:
        delete_order_dict = {}
        db = shelve.open('deleteorder.db', 'w')
        delete_order_dict = db['deleteOrder']
    except:
        print('error in opening delete db')
    
    deleted_orders = (deleted_order_id['order'].get_custOrder_id(),deleted_order_id['order'].get_status())
    delete_order_dict[deleted_order_id['order'].get_custOrder_id()] = deleted_orders
    
    db['deleteOrder'] = delete_order_dict 

    return redirect(url_for('retrieve_cust_orders'))




@app.route('/refundOrder/<uuid:id>', methods=['POST'])
@login_required
def refund_order(id):
    try:
        cust_order_dict = {}
        db = shelve.open('CustOrder.db', 'r')
        cust_order_dict = db['CustOrder']

        cust_order_list = []
        order = cust_order_dict.get(id)
        cust_order_list.append(order)

        db['CustOrder'] = cust_order_dict
        flash('Order has been deleted sucessfully')
    except:
        print('An error occured when opening CustOrder.db')
    finally:
        db.close()

    try:
        cust_order_dict = {}
        db = shelve.open('CustOrder.db', 'w')
        cust_order_dict = db['CustOrder']

        refund_order_id = cust_order_dict.get(id)
    
        refund_order_id['order'].set_status('Refunded')
        print(refund_order_id['order'].get_status())
        print(refund_order_id['order'].set_status('Refunded'))

        db['CustOrder'] = cust_order_dict
    except:
        print('An error occured when opening CustOrder.db')
    finally:
        db.close()
    
    try:
        delete_order_dict = {}
        db = shelve.open('deleteorder.db', 'w')
        delete_order_dict = db['deleteOrder']
    except:
        print('error in opening delete db')
 
    
    refund_orders = (refund_order_id['order'].get_custOrder_id(),refund_order_id['order'].get_status())
    delete_order_dict[refund_order_id['order'].get_custOrder_id()] = refund_orders
    
    db['deleteOrder'] = delete_order_dict 

    refund_mail2(id)
    
    flash('Order has been refunded sucessfully','success')

    return render_template('refund.html', count=len(cust_order_list), cust_order_list=cust_order_list)


def refund_mail2(id):
    try:
        cust_order_dict = {}
        db = shelve.open('CustOrder.db', 'r')
        cust_order_dict = db['CustOrder']
    except:
        print('error in opening db')
    finally:
        db.close()
    

    order = cust_order_dict.get(id)
    first_name_1 = order['order'].get_first_name()
    last_name_1 = order['order'].get_last_name()
    email = order['order'].get_email()

    sender = password = ""
    port = 465
    sender = 'testingusers1236@gmail.com'
    password = 'dG09#G.@Yg23G'

    recieve = 'tayzheyin123@gmail.com'
    first_name = first_name_1
    last_name = last_name_1

    

    msg = EmailMessage()
    msg['Subject'] = 'Chinese Arc Refund' + ' ( ' + first_name + last_name + ' ) '
    msg['From'] = sender
    msg['To'] = recieve

    

    

    msg.add_alternative("""\
    <!DOCTYPE html>
    <html lang="en">

    <body>
        <h3 style='color:black;'> Hey hey ~~ Hope your doing well! </h3>
        <h4> As requested by you, we have processed your refund and it should reflect in your bank account in the 2-3 business days.

    <br> <br> We are sad to see you go, but we hope that we could work together in the future where our product will be useful for your business.

    <br> <br> If you are still on the lookout for other options, please do let me know, as I’d be able to help you choose other options that might be the right fit for you.

    <br> <br> Please do stay connected. Have a great day.

    <br> <br> Thanks, </h4>
    <h3> Tay </h3>
    </body>
       

    </html>
    """, subtype='html')

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender, password)
        server.send_message(msg)

@app.route('/cust_order_history', methods = ['GET','POST'])
def cust_order_history():
    try:
        cust_order_dict = {}
        db = shelve.open('CustOrder.db', 'r')
        cust_order_dict = db['CustOrder']
    except:
        print('Unable to read data')
    finally:
        db.close()

    cust_order_list = []
    for key in cust_order_dict:
        cust_order = cust_order_dict.get(key)
        cust_order_list.append(cust_order)

    return render_template('cust_order_history.html', count=len(cust_order_list), cust_order_list=cust_order_list)

@app.route('/deliveredOrder/<uuid:id>', methods = ['POST'])
def delivered_order(id):
        delivered_order_dict = {}
        db = shelve.open('deliveredorder.db', 'c')
        try:
            delivered_order_dict = db['deliveredOrder']
        except:
            print('Error in opening db')
        
        db['deliveredOrder'] = delivered_order_dict
        db.close()


        try:
            cust_order_dict = {}
            db = shelve.open('CustOrder.db', 'r')
            cust_order_dict = db['CustOrder']

            cust_order_list = []
            order = cust_order_dict.get(id)
            cust_order_list.append(order)

            db['CustOrder'] = cust_order_dict
            flash('Order has been deleted sucessfully')
        except:
            print('An error occured when opening CustOrder.db')
        finally:
            db.close()

        try:
            cust_order_dict = {}
            db = shelve.open('CustOrder.db', 'w')
            cust_order_dict = db['CustOrder']

            delivered_order_id = cust_order_dict.get(id)
        
            delivered_order_id['order'].set_status('Delivered')
            print(delivered_order_id['order'].get_status())
            print(delivered_order_id['order'].set_status('Delivered'))

            db['CustOrder'] = cust_order_dict
        except:
            print('An error occured when opening CustOrder.db')
        finally:
            db.close()
        
        try:
            delete_order_dict = {}
            db = shelve.open('deleteorder.db', 'w')
            delete_order_dict = db['deleteOrder']
        except:
            print('error in opening delete db')
    
        
        delivered_orders = (delivered_order_id['order'].get_custOrder_id(),delivered_order_id['order'].get_status())
        delete_order_dict[delivered_order_id['order'].get_custOrder_id()] = delivered_orders
        
        db['deleteOrder'] = delete_order_dict 

        return render_template('cust_order_history.html', count=len(cust_order_list), cust_order_list=cust_order_list)

@app.route('/fullpage_cart')
def fullpage_cart():
    try:
        voucher_dict = {}
        db = shelve.open('voucher.db', 'r')
        voucher_dict = db['Vouchers']
    except(IOError):
        print('Unable to read data')
    finally:
        db.close()
    voucher_list = []
    for key in voucher_dict:
        order = voucher_dict.get(key)
        voucher_list.append(order)

    return render_template('fullpage_cart.html',count=len(voucher_list),voucher_list=voucher_list)

@app.route('/order_confirm')
def order_confirm():

    try:
        cust_cart_dict = {}
        db = shelve.open('custCart.db', 'r')
        cust_cart_dict = db['custCart']

        print(cust_cart_dict)
      
    except:
        print('Error in opening db')

    cust_cart_list = []
    for key in cust_cart_dict:
        cust_cart = cust_cart_dict.get(key)
        cust_cart_list.append(cust_cart)
    
    try:
        cust_cart_dict = {} 
        db = shelve.open('custCart.db', 'w')
        cust_cart_dict = db['custCart']

        cust_cart_dict.clear()

        db['custCart'] = cust_cart_dict
    except:
        print('An error occured when opening CustOrder.db')
    finally:
        db.close()
    try:
        cust_order_dict = {}
        db = shelve.open('CustOrder.db', 'r')
        cust_order_dict = db['CustOrder']
    except:
        print('Unable to read data')
    finally:
        db.close()

    cust_order_list = []
    for key in cust_order_dict:
        cust_order = cust_order_dict.get(key)
        cust_order_list.append(cust_order)
    return render_template('orderConfirm.html',count=len(cust_order_list), cust_order_list=cust_order_list, count2=len(cust_cart_list),cust_cart_list=cust_cart_list)

@app.route('/fullpage_wish')
def fullpage_wish():
   
    return render_template('fullpage_wish.html')

# Contact Us(Enquiry): create
@app.route('/createContact', methods=['GET', 'POST'])
def create_contact():
    create_contact_form = CreateContactForm(request.form)
    if request.method == 'POST' and create_contact_form.validate():
        contact_dict = {}
        db = shelve.open('contact.db', 'c')

        try:
            contact_dict = db['Contact']
        except:
            print("Error in retrieving Contact from contact.db.")

        contact = Contact(create_contact_form.first_name.data, 
                            create_contact_form.last_name.data, 
                            create_contact_form.email.data, 
                            create_contact_form.subject.data, 
                            create_contact_form.message.data)

        contact_dict[contact.get_contact_id()] = contact
        db['Contact'] = contact_dict

        db.close()

        flash("Your enquiry has been sent succesfully. Please look out for a email from us soon.", "success")

        return redirect(url_for('home_page'))
    return render_template('createContact.html', form=create_contact_form)

# Contact Us(Enquiry): retrieve
@app.route('/retrieveContact')
def retrieve_contact():
    try:
        contact_dict = {}
        db = shelve.open('contact.db', 'r')
        contact_dict = db['Contact']

    except(IOError):
        print('Unable to read data')

    finally:
        db.close()

    contact_list = []
    for key in contact_dict:
        contact = contact_dict.get(key)
        contact_list.append(contact)

    adjustment_list = []
    for key in contact_dict:
        adjustment = contact_dict.get(key)
        if adjustment.get_subject() == 'Cheongsam Adjustment':
            adjustment_list.append(adjustment)

    sizing_list = []
    for key in contact_dict:
        sizing = contact_dict.get(key)
        if sizing.get_subject() == 'Sizing':
            sizing_list.append(sizing)

    appointment_list = []
    for key in contact_dict:
        appointment = contact_dict.get(key)
        if appointment.get_subject() == 'Appointment':
            appointment_list.append(appointment)

    others_list = []
    for key in contact_dict:
        others = contact_dict.get(key)
        if others.get_subject() == 'Others':
            others_list.append(others)        

    return render_template('retrieveContact.html', 
                            count=len(contact_list), 
                            contact_list=contact_list, 
                            adjustment_list=adjustment_list,
                            count1=len(adjustment_list),
                            sizing_list=sizing_list,
                            count2=len(sizing_list),
                            appointment_list=appointment_list,
                            count3=len(appointment_list),
                            others_list=others_list,
                            count4=len(others_list)
                            )

# Contact Us(Enquiry): reply to customer's enquiry + delete enquiry
@app.route('/createContactReply/<uuid:id>/', methods=['GET', 'POST'])
def create_contactReply(id):
    create_contactReply_form = CreateContactReplyForm(request.form)
    if request.method == 'POST' and create_contactReply_form.validate():
        contactReply_dict = {}
        db = shelve.open('contactReply.db', 'c')

        try:
            contactReply_dict = db['ContactReply']
        except:
            print("Error in retrieving ContactReply from contactReply.db.")

        contactReply = ContactReply(create_contactReply_form.reply.data, 
                                    create_contactReply_form.create_by.data, 
                                    create_contactReply_form.create_date.data)
        contactReply_dict[contactReply.get_contactReply_id()] = contactReply
        db['ContactReply'] = contactReply_dict
        db.close()

        #send email reply
        contactReply_email(id)

        # deleting the query after reply
        try:
            contact_dict = {}
            db = shelve.open('contact.db', 'w')
            contact_dict = db['Contact']

            contact_dict.pop(id)

            db['Contact'] = contact_dict

        except(IOError):
            print('Unable to read data')

        finally:
            db.close()

        return redirect(url_for('retrieve_contact'))
    return render_template('createContactReply.html', form=create_contactReply_form)

# Contact Us(Enquiry): email
def contactReply_email(id):
    try:
        contact_dict = {}
        db = shelve.open('contact.db', 'r')
        contact_dict = db['Contact']

        contactReply_dict = {}
        db = shelve.open('contactReply.db', 'r')
        contactReply_dict = db['ContactReply']

    except:
        print('An error occuured while opeing DB')

    finally:
        db.close()

    contact = contact_dict.get(id)
    contactReply = contactReply_dict.get(id)
    if contact == contactReply:
        contact.email.data = contact.get_email()
        contact.subject.data = contact.get_subject()
        contact.first_name.data = contact.get_first_name()
        contact.last_name.data = contact.get_last_name()

    for key in contactReply_dict:
        contactReply = contactReply_dict.get(key)
        reply = contactReply.get_reply()

    sender = password = ""
    port = 465
    sender = 'testingusers1236@gmail.com'
    password = 'dG09#G.@Yg23G'

    reciever = contact.get_email()
    first_name = contact.get_first_name()
    last_name = contact.get_last_name()

    message = MIMEMultipart("alternative")
    message["Subject"] = 'The Chinese Arc Query Reply: ' + contact.get_subject()
    message["From"] = sender
    message["To"] = reciever

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(reply, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender, password)
        server.sendmail(
            sender, reciever, message.as_string()
        )

# Full product page
@app.route('/fullProduct/<int:id>')
def full_product_page(id):
    try:
        productinfo_dict = {}
        db = shelve.open('ProductInfo.db', 'r')
        productinfo_dict = db['ProductInfo']
    except IOError:
        print('An error occurred trying to read from ProductInfo.db')
    else:
        db.close()
    
    productinfo_list = []
    for key in productinfo_dict:
        productinfo = productinfo_dict.get(key)
        if productinfo.get_product_category() == 'Cheongsam':
            if productinfo.get_product_id() == id:
                productinfo_list.append(productinfo)

        elif productinfo.get_product_category() == 'TangZhuang':
            if productinfo.get_product_id() == id:
                productinfo_list.append(productinfo)

        elif productinfo.get_product_category() == 'Accessories':
            if productinfo.get_product_id() == id:
                productinfo_list.append(productinfo)

        elif productinfo.get_product_category() == 'Featured':
            if productinfo.get_product_id() == id:
                productinfo_list.append(productinfo)

    image_list = os.listdir(app.config['UPLOADED_PHOTOS_DEST'])

    return render_template('fullProduct_page.html',
                            count1=len(image_list),
                            count2=len(productinfo_list),
                            productinfo_list = productinfo_list,
                            image_list = image_list,
                            )

if __name__ == '__main__':
    app.run(debug=True)