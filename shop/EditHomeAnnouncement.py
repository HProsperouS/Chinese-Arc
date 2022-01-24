import datetime
from wtforms import Form, TextAreaField, validators, StringField,DateField
class CreateHomeAnnouncementForm(Form):
    title = StringField('Title', [validators.DataRequired()])
    text = TextAreaField('Text', [validators.DataRequired()])
    create_date= DateField("Date of Creation",[validators.DataRequired()],format="%Y-%m-%d", default=datetime.datetime.now())
    create_by= StringField('Created by', [validators.Length(min=1, max=150), validators.DataRequired()])
    modified_date = DateField("Date of Modification",[validators.Optional()])
    modified_by = StringField('Modified by', [validators.Length(min=1, max=150), validators.Optional()],default='None')

class UpdateHomeAnnouncementForm(Form):
    title = StringField('Title', [validators.DataRequired()])
    text = TextAreaField('Text', [validators.DataRequired()])
    create_date= DateField("Date of Creation",[validators.Optional()],format="%Y-%m-%d")
    create_by= StringField('Created by', [validators.Length(min=1, max=150), validators.Optional()])
    modified_date = DateField("Date of Modification",[validators.DataRequired()],format="%Y-%m-%d", default=datetime.datetime.now())
    modified_by = StringField('Modified by', [validators.Length(min=1, max=150), validators.DataRequired()] )
