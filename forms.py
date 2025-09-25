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


class SetupDriverForm(FlaskForm):
    driver_name = StringField("Enter name", validators=[DataRequired()])
    driver_number = StringField("Enter driver number", validators=[DataRequired()])
    line_number = StringField("Enter current line number", validators=[DataRequired()])

    submit = SubmitField()
