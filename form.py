from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    first_name = StringField('Имя', validators=[DataRequired()])
    last_name = StringField('Фамилия', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


# class RegisterForm(FlaskForm):
#     name = StringField("Имя: ", validators=[Length(min=4, max=100, message="Имя должно быть от 4 до 100 символов")])
#     email = StringField("Email: ", validators=[Email("Некорректный email")])
#     psw = PasswordField("Пароль: ", validators=[DataRequired(),
#                                                 Length(min=4, max=100, message="Пароль должен быть от 4 до 100 символов")])

#     psw2 = PasswordField("Повтор пароля: ", validators=[DataRequired(), EqualTo('psw', message="Пароли не совпадают")])
#     submit = SubmitField("Регистрация")