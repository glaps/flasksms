from wtforms import Form, BooleanField, StringField, PasswordField, FileField


class loginf(Form):
    mail = StringField()
    passw = PasswordField()
    remember = BooleanField('remembere', default = False)

class getf(Form):
    file = FileField()
    msg = StringField()
    num = StringField()
