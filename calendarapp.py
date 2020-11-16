from flask import Flask, render_template, url_for
app = Flask(__name__)

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
        1 : "January",
        2 : "February",
        3 : "March",
        4 : "April",
        5 : "May",
        6 : "June",
        7 : "July",
        8 : "August",
        9 : "September",
        10 : "October",
        11 : "November",
        12 : "December"
        }

month_len = {
        "January" : 31,
        "February": 28,
        "March" : 31,
        "April" : 30,
        "May" : 31,
        "June" : 30,
        "July" : 31,
        "August" :31,
        "September" : 30,
        "October" : 31,
        "November" : 30,
        "December" : 31
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


@app.route("/")
@app.route("/home")
def hello():
    return render_template("layout.html")


@app.route("/calendar/<int:year>-int:week>")
def calendar(year, week):
    info = {
            "year" : year,
            "week" : week,
            }



    return render_template("calendar.html", info=info) 
