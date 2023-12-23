from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.fields import StringField, SubmitField, PasswordField, RadioField, DateField, SelectField, FileField
from wtforms.validators import DataRequired, InputRequired, Length, Email, EqualTo

class AddCommentForm(FlaskForm):
    name = StringField('თქვენი სახელი', validators=[InputRequired()])
    comment = StringField('დაამატეთ კომენტარი', validators=[InputRequired()])
    submit = SubmitField('დამატება' )
    
class AddProduct(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    img = FileField('Image', validators=[FileRequired(), FileAllowed(['jpeg', 'jpg', 'png'])])
    submit = SubmitField('Add Product')
    
class EditProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    img = FileField('Product Image')
    submit = SubmitField('Update Product')

class RemoveProductForm(FlaskForm):
    submit = SubmitField('Remove Product', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    repeat_password = PasswordField('Repeat Password', validators=[InputRequired(), EqualTo('password')])
    gender = RadioField("Gender", choices=[('male', 'Male'), ('female', 'Female')], validators=[InputRequired()])
    birthday = DateField('Date of Birth', format='%Y-%m-%d', validators=[InputRequired()])
    country = SelectField('Country', choices=[('georgia', 'Georgia'), ('usa', 'USA')], validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    submitt = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Login')

