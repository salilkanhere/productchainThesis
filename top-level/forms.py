from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

class CreateForm(FlaskForm):
    regions = [('Rural', 'rural'), ('Urban', 'urban')]
    batch_id = StringField('Batch ID', validators=[DataRequired()])
    region = SelectField('Region', choices = regions, validators = [DataRequired()])
    owner = StringField('Owner', validators=[DataRequired()])
    product_type = StringField('Product Type', validators=[DataRequired()])
    constituents = StringField('Constituents')

    submit = SubmitField('Create')




class TransferForm(FlaskForm):
    regions = ['Rural', 'Urban']
    batch_id = StringField('Batch ID', validators=[DataRequired()])
    region = SelectField(u'Region', choices = regions, validators = [DataRequired()])
    owner = StringField('New Owner', validators=[DataRequired()])
    product_type = StringField('Product Type', validators=[DataRequired()])

    submit = SubmitField('Transfer')




class StoryQueryForm(FlaskForm):
    batch_id = StringField('Batch ID', validators=[DataRequired()])

    submit = SubmitField('Query')