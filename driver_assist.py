from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import CSRFProtect
from flask_bootstrap import Bootstrap5
from roster import *
from datetime import date, timedelta
from forms import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'roundabout'
csrf = CSRFProtect(app)
bootstrap = Bootstrap5(app)

line_number = "3801"
current_week = get_weeks(line_number, 5).to_html(classes="table table-striped, text-end", border=1, index=False)
date_today = date.today()
@app.route("/")
def dashboard():
    return render_template("dashboard/dashboard.html", roster=current_week, date=date_today)

@app.route("/check/week", methods=["POST", "GET"])
def check_week():
    form = CheckWeekForm()
    check_roster = None
    if form.validate_on_submit():
        check_date = form.data["date"]
        flash(f"{check_date}", "success")
        if check_date.weekday() == 6:
            recent_sunday = check_date
        else:
            days_since_sunday = check_date.weekday() + 1
            recent_sunday = check_date - timedelta(days=days_since_sunday)
        check_line = get_line_from_date(today_date=date_today, target_date=recent_sunday, current_line=line_number)
        check_roster = get_line(check_line).to_html(classes="table table-striped, text-end", border=1, index=False)


    return render_template("check_week/check_week.html", form=form, check_roster=check_roster)

@app.route("/check/duty", methods=["POST", "GET"])
def check_duty():
    form = CheckDutyForm()
    duty = None
    if form.validate_on_submit():
        duty_number = form.data["duty"]
        duty = get_duty(duty_number).to_html(classes="table table-striped, text-end", border=1, index=False)

    return render_template("check_duty/check_duty.html", form=form, check_duty=duty)


@app.route("/edit/line_number", methods=["POST", "GET"])
def edit_line_number():
    form = EditLineNumber()
    if form.validate_on_submit():
        global line_number
        line_number = form.data["line_number"]
        return redirect(url_for("dashboard"))

    return render_template("edit/edit_line_number.html", form=form)

app.run(debug=True)
