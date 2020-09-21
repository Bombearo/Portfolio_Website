from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, BooleanField, MultipleFileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from portfolio_app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class EditAboutForm(FlaskForm):
    first_line = StringField('Opening', validators=[DataRequired(), Length(min=10,max=100)])
    about = TextAreaField('About Description', validators=[DataRequired(),], render_kw={'rows':'4','cols':'100','maxlength':4000})
    profile_pic = FileField('Insert Image:', validators=[FileAllowed(['jpg','png'])])
    button_1_link = StringField('Link for first Button')
    button_1_text = StringField('Text on first button')
    button_2_link = StringField('Link for second Button')
    button_2_text = StringField('Text on second Button')
    submit = SubmitField('Update')


class PortfolioForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Project Description (500 Chars)', validators=[DataRequired()], render_kw={'maxlength':500})
    github_link = StringField('Insert Link to Github: ', validators=[DataRequired()])
    thumbnails = MultipleFileField('Upload new Thumbnails (1028x720px recommended - unable to change): ', render_kw={'multiple':True})
    tags = StringField('Tags (Enter keywords separated by spaces for your project)')
    submit = SubmitField('Post')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username - Used for logging in to your admin page',validators=[DataRequired(), Length(min=2, max=20)])
    name = StringField('Name/Alias - This will be used in your navbar, and on the front page of your website.', validators=[DataRequired(), Length(min=2, max=30)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    password = PasswordField('New Password')
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class ConfirmChanges(FlaskForm):
    password = PasswordField('Enter password to confirm changes', validators=[DataRequired()])
    submit = SubmitField('Confirm Changes')

class UpdateContactForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Length(min=2, max=50),Email()])
    github_profile = StringField('Enter your Github username', validators=[DataRequired()])
    submit=SubmitField('Update Contacts')