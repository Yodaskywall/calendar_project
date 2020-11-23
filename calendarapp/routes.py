import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from calendarapp import app, db, bcrypt
from calendarapp.models import User, Event
from flask_login import login_user, current_user, logout_user, login_required

month_to_num = {
        "January" : 1,
        "February": 2,
        "March" : 3,
        "April" : 4,
        "May" : 5,
        "June" : 6,
        "July" : 7,
        "August" : 8,
        "September" : 9,
        "October" : 10,
        "November" : 11,
        "December" : 12
        }

num_to_month = {
        1 : "Jan",
        2 : "Feb",
        3 : "Mar",
        4 : "Apr",
        5 : "May",
        6 : "Jun",
        7 : "Jul",
        8 : "Aug",
        9 : "Sep",
        10 : "Oct",
        11 : "Nov",
        12 : "Dec"
        }

month_len = {
        1 : 31,
        2 : 28,
        3 : 31,
        4 : 30,
        5 : 31,
        6 : 30,
        7 : 31,
        8 :31,
        9 : 30,
        10 : 31,
        11 : 30,
        12 : 31
        }

# 2020, 2021, 2022, 2023, 2024, 2025, ..., n
# 2, 4, 5, 6, 0, 2


def get_c(year):
    c = 2
    
    for yr in range(2021,year+1):
        if (yr-1) % 4 == 0:
            c += 2

        else:
            c += 1

        if c > 6:
            c= c % 6 - 1

    return c


def get_mon_day(day, year):
    for month in range(1,13):
        if month == 2 and year % 4 == 0:
            if day > 29:
                day -= 29

            else:
                return day, month

        else:
            if day > month_len[month]:
                day -= month_len[month]

            else:
                return day, month

print(get_mon_day(17, 2020))

def get_week(year, week):
    c = get_c(year)



@app.route("/")
@app.route("/home")
def hello():
    return "Home"

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash("Account created for {form.username.data}!", "success")
        return redirect(url_for("home"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@blog.com" and form.password.data == "password":
            flash("You have been logged in!", "success")
            return redirect(url_for("home"))

        else:
            flash("Login Unsuccessful. Please check username and password", "danger")
        return render_template("login.html", form=form)

@app.route("/<int:year>-<int:week>")
def calendar(year, week):
    day_n = week * 7 - get_c(year)
    days = [[get_mon_day(d, year)[0],
       num_to_month[get_mon_day(d, year)[1]]] for d in range(day_n+1, day_n+8)]
    
    for i in range(len(days)):
        if days[i][0] <= 0:
            if (year-1) % 4 == 0:
                d_ = 366 + days[i][0]
            
            else:
                d_ = 365 + days[i][0]
            
            day_, month_ = get_mon_day(d_, year-1)
            days[i] = [day_, num_to_month[month_]]
    
    info = {
            "year" : year,
            "week" : week,
            "days" : days
            }



    return render_template("calendar.html", info=info) 