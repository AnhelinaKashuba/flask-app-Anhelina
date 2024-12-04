from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, SelectField, DateField
from wtforms.validators import DataRequired, Length

# Категорії для SelectField
CATEGORIES = [
    ('tech', 'Technology'),
    ('life', 'Lifestyle'),
    ('edu', 'Education'),
    ('other', 'Other')
]

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    content = TextAreaField('Content', validators=[DataRequired()])
    is_active = BooleanField('Active Post')
    publish_date = DateField('Publish Date', 
                             format='%Y-%m-%d', validators=[DataRequired()])
    category = SelectField('Category', 
                           choices=CATEGORIES, validators=[DataRequired()])
    submit = SubmitField('Submit')
