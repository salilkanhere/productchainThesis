from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class CreateForm(FlaskForm):
    batch_id = StringField('Batch ID', validators=[DataRequired()])
    region = StringField('Region', validators=[DataRequired()])
    owner = StringField('Owner', validators=[DataRequired()])
    product_type = StringField('Product Type', validators=[DataRequired()])
    constituents = StringField('Constituents')

    submit = SubmitField('Create')




class TransferForm(FlaskForm):
    batch_id = StringField('Batch ID', validators=[DataRequired()])
    region = StringField('Region', validators=[DataRequired()])
    owner = StringField('New Owner', validators=[DataRequired()])
    product_type = StringField('Product Type', validators=[DataRequired()])

    submit = SubmitField('Transfer')




class StoryQueryForm(FlaskForm):
    batch_id = StringField('Batch ID', validators=[DataRequired()])

    submit = SubmitField('Query')