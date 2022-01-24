from wtforms import Form, StringField, SelectField,HiddenField,validators,IntegerField, DateField

import datetime

class CreateVoucherForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired(message='Alphabets only')])
    desc = StringField('Description', [validators.Length(min=1, max=150), validators.DataRequired()])
    type = SelectField('Voucher Type', [validators.DataRequired(message='Please choose voucher type')], choices=[('', 'N/A'), ('Cashback', 'Cashback'), ('Discount', 'Discount')], default='')
    total = IntegerField('Limit', [validators.DataRequired(message='Numbers only')])
    status = SelectField('Status', [validators.DataRequired(message='Please choose status')], choices=[('', 'N/A'), ('Active', 'Active'), ('Expired', 'Expired')], default='')
    date = DateField("Start",[validators.DataRequired(message='Do not change')],format="%Y-%m-%d", default=datetime.datetime.now())
    end_date = DateField("End",[validators.DataRequired(message='Do not change')],format="%Y-%m-%d", default=datetime.datetime.now())
    create_date = DateField("Date of Creation",[validators.DataRequired()],format="%Y-%m-%d", default=datetime.datetime.now())
    create_by = StringField('Created by', [validators.Length(min=1, max=150), validators.DataRequired()])
    mod_date = DateField("Date of Modification",[validators.Optional()])
    mod_by = StringField('Modified by', [validators.Length(min=1, max=150), validators.Optional()],default='None')

class UpdateVoucherForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired(message='Alphabets only')])
    desc = StringField('Description', [validators.Length(min=1, max=150), validators.DataRequired()])
    type = SelectField('Voucher Type', [validators.DataRequired(message='Please choose voucher type')], choices=[('', 'N/A'), ('Cashback', 'Cashback'), ('Discount', 'Discount')], default='')
    total = IntegerField('Limit', [validators.DataRequired(message='Numbers only')])
    status = SelectField('Status', [validators.DataRequired(message='Please choose status')], choices=[('', 'N/A'), ('Active', 'Active'), ('Expired', 'Expired')], default='')
    date = DateField("Start",[validators.DataRequired(message='Do not change')],format="%Y-%m-%d", default=datetime.datetime.now())
    end_date = DateField("End",[validators.DataRequired(message='Do not change')],format="%Y-%m-%d", default=datetime.datetime.now())
    create_date = DateField("Date of Creation",[validators.Optional()],format="%Y-%m-%d")
    create_by = StringField('Created by', [validators.Length(min=1, max=150), validators.Optional()])
    mod_date = DateField("Date of Modification",[validators.DataRequired()],format="%Y-%m-%d", default=datetime.datetime.now())
    mod_by = StringField('Modified by', [validators.Length(min=1, max=150), validators.DataRequired()] )
