from flask import Flask, render_template, request,session
from db import Database
from datetime import date
from summerizer import Summarizer
app=Flask(__name__)
app.secret_key = 'secret'
summarizer=Summarizer()
@app.route("/")
def base():
    return render_template("base.html")

@app.route("/login" ,methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form.get("name")
        session["username"]=username
        pin=request.form.get("pin")
        if Database().check_user(username,pin):
            return render_template("decision.html")
        else:
            return render_template("login.html",error=True)
    return render_template("login.html")

@app.route("/signin", methods=["GET","POST"])
def signin():
    if request.method=="POST":
        username=request.form.get("name")
        session["username"]=username
        pin=request.form.get("pin")
        Database().add_user(username,pin,date.today())
        return render_template("setup.html")
    return render_template("signin.html")

@app.route("/setup", methods=["GET","POST"])
def setup():
    if request.method=="POST":
        delete=request.form.get("del")
        if delete:
            Database().delete_tasks(delete)
        else:
            task=request.form.get("task")
            start=f"{request.form.get("start-hrs")}:{request.form.get("start-min") or "00"}"
            end=f"{request.form.get("end-hrs")}:{request.form.get("end-min") or "00"}"
            Database().add_task(session.get("username"),task,start,end)
    return render_template("setup.html",data=Database().fetch_tasks(session.get("username")),username=session.get("username"))

@app.route("/dashboard", methods=["GET","POST"])
def dashboard():
    if request.method=="POST":
        for checked in request.form:
            Database().add_checks(session.get("username"),checked,date.today())
    return render_template("dashboard.html",date=date.today(),data=Database().fetch_tasks(session.get("username")),username=session.get("username"))

@app.route("/history", methods=["GET","POST"])
def history():
    if request.method=="POST":
        form_date=request.form.get("date")
        checks=Database().get_checks(session.get("username"),form_date)
        data=Database().fetch_tasks(session.get("username"))
        return render_template("history.html",today=date.today(),first=Database().get_first_date(session.get("username")),checks=checks,data=data)
    return render_template("history.html",today=date.today(),first=Database().get_first_date(session.get("username")))

@app.route("/summary")
def summary():
    tasks=Database().fetch_tasks(session.get("username"))
    checks=Database().get_all_checks(session.get("username"))
    data=[[row['id'],row['task'],row['start'],row['end']] for row in tasks]
    summary=summarizer.summarize(data,checks)
    return render_template("summary.html",summary=summary)

app.run()