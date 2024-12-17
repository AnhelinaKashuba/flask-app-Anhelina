from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, SelectField, DateField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed
from app.posts.models import User 
from .models import Tag 
from wtforms import SelectMultipleField


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
    publish_date = DateField('Publish Date', format='%Y-%m-%d', validators=[DataRequired()])
    category = SelectField('Category', choices=CATEGORIES, validators=[DataRequired()])
    image = FileField('Post Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])

    # Manually populate author options
    author_id = SelectField("Author", coerce=int, validators=[DataRequired()])
    
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.author_id.choices = [(user.id, user.username) for user in User.query.all()]

    tags = SelectMultipleField(
        "Tags", 
        coerce=int, 
        choices=[(tag.id, tag.name) for tag in Tag.query.all()]
    )

    submit = SubmitField('Submit')

    

    


