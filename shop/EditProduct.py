from logging import PlaceHolder
from wtforms import Form, TextAreaField, StringField,validators
from wtforms.fields.core import DateField, IntegerField,FloatField,datetime,SelectField
from flask_wtf.file import FileField, FileRequired,FileAllowed
from flask_uploads import UploadSet, IMAGES

photos = UploadSet('photos', IMAGES)
class CreateProductForm(Form):
    product_image = FileField('Product Image', validators=[FileAllowed(['jpeg','jpg','png','gif']), FileRequired(message='File required')])
    product_name = StringField('Product Name', [validators.Length(min=1, max=50), validators.DataRequired(message='String only')])
    product_category = SelectField('Product Category', [validators.DataRequired()], choices=[('Featured', 'Featured'), ('Cheongsam', 'Cheongsam'), ('TangZhuang', 'TangZhuang'),('Accessories', 'Accessories')] ,default='Featured')
    product_price= FloatField('Product Price', [validators.NumberRange(min=1, max=999, message='Product price must in a range of 1 - 999'), validators.DataRequired()])
    product_description= TextAreaField('Product Description', [validators.Length(min=1, max=3000),validators.DataRequired()])
    # cannot less than 1 for price and stock
    product_stock= IntegerField('Product Stock', [validators.NumberRange(min=1, max=999, message='Product price must in a range of 1 - 999'),validators.DataRequired()])
    create_date= DateField("Date of Creation",[validators.DataRequired()],format="%Y-%m-%d", default=datetime.datetime.now())
    create_by= StringField('Created by', [validators.Length(min=1, max=150), validators.DataRequired()])
    modified_date = DateField("Date of Modification",[validators.Optional()])
    modified_by = StringField('Modified by', [validators.Length(min=1, max=150), validators.Optional()],default='None')

class UpdateProductForm(Form):
   product_image = FileField('Product Image', validators=[FileAllowed(['jpeg','jpg','png','gif']), FileRequired()])
   product_name = StringField('Product Name', [validators.Length(min=1, max=50), validators.DataRequired()])
   product_category = SelectField('Product Category', [validators.DataRequired()], choices=[('Featured', 'Featured'), ('Cheongsam', 'Cheongsam'), ('TangZhuang', 'TangZhuang'),('Accessories', 'Accessories') ], default='Featured')
   product_price= FloatField('Product Price', [validators.NumberRange(min=1, max=999, message='Product price must in a range of 1 - 999'), validators.DataRequired()])
   product_description= TextAreaField('Product Description', [validators.Length(min=1, max=300),validators.DataRequired()])
   #  cannot less than 1 for price and stock
   product_stock= IntegerField('Product Stock', [validators.NumberRange(min=1, max=999, message='Product price must in a range of 1 - 999'),validators.DataRequired()])
   create_date= DateField('Date Of Creation', format="%Y-%m-%d", default=datetime.datetime.now())
   create_by= StringField('Created by', [validators.Length(min=1, max=150), validators.Optional()])
   modified_date = DateField("Date Of Modification",[validators.DataRequired()],format="%Y-%m-%d", default=datetime.datetime.now())
   modified_by = StringField('Modified by', [validators.Length(min=1, max=150), validators.DataRequired()] )