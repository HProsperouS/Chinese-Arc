from email import message
import email
from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, PasswordField,IntegerField,DateTimeField,FloatField, BooleanField,DateTimeField
import datetime
from wtforms.fields.html5 import EmailField ,DateField
from wtforms.widgets import PasswordInput

class CreateCustOrder(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email Address', [validators.DataRequired(message='Please enter a valid email address')])
    card_num = IntegerField('Card Number', [validators.DataRequired(message='Please enter the 16-digit card number')])
    card_type = SelectField('Card Type', [validators.DataRequired(message='Please choose card type')], choices=[('Select', 'Select'), ('Visa', 'Visa'), ('Mastercard', 'Mastercard')], default='')
    holder_name = StringField('Card Holder Name', [validators.Length(min=1, max=150), validators.DataRequired(message='This field is required')])
    cvv = PasswordField('CVV', [validators.Length(min=3,max=3), validators.DataRequired(message='First 3 Numbers only')])
    city = SelectField('City', [validators.Length(max=200), validators.DataRequired()],choices=[('', 'Select'), ('Singapore', 'Singapore'), ('Malaysia', 'Malaysia'),('USA', 'America')], default='')
    postal_code = IntegerField('Postal Code', [validators.DataRequired(message='Numbers only')])
    unit_number = StringField('Unit Number',  [validators.DataRequired(message = "Enter valid Unit Number please")])
    
    create_date= DateField('Date Created', [validators.DataRequired()],format="%Y-%m-%d", default=datetime.datetime.now())
    modified_by = StringField('Modified By', [validators.Length(min=1, max=50), validators.Optional()])
    modified_date = DateField('Modified Date', [validators.Optional()])
    status = SelectField('Status', [validators.DataRequired(message='Please choose card type')], choices=[('Pending', 'Pending'), ('Undelivered', 'Undelivered'), ('Delivered', 'Delivered')], default='Pending')

class CustOrderUpdate(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired(message='Please enter a valid name')])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired(message='Please enter a valid name')])
    email= StringField('Email Address', [validators.Email(), validators.DataRequired(message='Please enter a valid email')])
    
    card_num = IntegerField('Card Number', [validators.DataRequired(message='Numbers only')])
    card_type = SelectField('Card Type', [validators.DataRequired(message='Please choose card type')], choices=[('Select', 'Select'), ('Visa', 'Visa'), ('Mastercard', 'Mastercard')], default='')

    holder_name = StringField('Card Holder Name', [validators.Length(min=1, max=150), validators.DataRequired(message='Please enter a valid name')])
    postal_code = IntegerField('Postal Code', [validators.DataRequired(message='Numbers only')])
    unit_number = StringField('Unit Number',  [validators.DataRequired(message = "Enter valid Unit Number please")])
    city = SelectField('City', [validators.Length(max=200), validators.DataRequired()],choices=[('', 'Select'), ('Singapore', 'Singapore'), ('Malaysia', 'Malaysia'),('USA', 'America')], default='')
    
    create_date= DateField('Date Created',[validators.Optional()], format="%Y-%m-%d")
    modified_by = StringField('Modified By', [validators.Length(min=1, max=50), validators.DataRequired(message='Enter admin name')],default='Jo')
    modified_date = DateField('Modified Date',[validators.DataRequired()],  format='%Y-%m-%d',default=datetime.datetime.now())