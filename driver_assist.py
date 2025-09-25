from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import CSRFProtect
from flask_bootstrap import Bootstrap5
from roster import *
from datetime import date, timedelta
from forms import *
from dev_tools import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'roundabout'
csrf = CSRFProtect(app)
bootstrap = Bootstrap5(app)


@app.route("/")
@driver_handle()
def dashboard():
    driver_service = get_driver_service()
    date_today = driver_service.date_today.strftime("%d/%m/%Y")

    driver_data = driver_service.driver_repository.driver_data
    show_roster = driver_service.retrieve_roster_weeks(weeks=5).to_html(
        classes="table table-striped, text-end", border=1, index=False)

    return render_template("/pages/dashboard.html", roster=show_roster, date=date_today, driver=driver_data)


@app.route("/setup/driver", methods=["POST", "GET"])
def setup_driver():
    driver_service = get_driver_service()
    form = SetupDriverForm()
    if form.validate_on_submit():
        name, number, line_number = form.data["driver_name"], form.data["driver_number"], form.data["line_number"]
        driver_service.setup_new_driver(name=name, number=number, line_number=line_number)
        return redirect(url_for("dashboard"))

    return render_template("pages/setup_driver.html", form=form)


@app.route("/check/week", methods=["POST", "GET"])
@driver_handle()
def check_week():
    driver_service = get_driver_service()

    form = CheckWeekForm()
    check_roster = None
    if form.validate_on_submit():
        check_date = form.data["date"]
        flash(f"{check_date}", "success")
        check_roster = driver_service.retrieve_line_from_date(check_date).to_html(
            classes="table table-striped, text-end", border=1, index=False)

    return render_template("pages/check_week.html", form=form, check_roster=check_roster)


@app.route("/check/duty", methods=["POST", "GET"])
@driver_handle()
def check_duty():
    driver_service = get_driver_service()

    form = CheckDutyForm()
    duty = None
    if form.validate_on_submit():
        duty_number = form.data["duty"]

        duty = driver_service.retrieve_duty(duty_number).to_html(
            classes="table table-striped, text-end", border=1, index=False)

    return render_template("pages/check_duty.html", form=form, check_duty=duty)


@app.route("/edit/line_number", methods=["POST", "GET"])
@driver_handle()
def edit_line_number():
    form = EditLineNumber()
    driver_service = get_driver_service()
    if form.validate_on_submit():
        line_number = form.data["line_number"]
        driver_service.update_line_number(line_number)
        return redirect(url_for("dashboard"))

    return render_template("forms/edit_line_number.html", form=form)


app.run(debug=True)
