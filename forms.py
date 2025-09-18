from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length


class CheckWeekForm(FlaskForm):
    date = DateField()

    submit = SubmitField()

class CheckDutyForm(FlaskForm):
    duty = StringField("Enter duty number")

    submit = SubmitField()

class EditLineNumber(FlaskForm):
    line_number = StringField("Enter new line number")

    submit = SubmitField()
