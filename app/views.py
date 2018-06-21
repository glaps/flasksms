import os
from app import app
from flask import render_template as re_t
from flask import request, session, redirect,url_for
from werkzeug.utils import secure_filename
from app import forms
from conf import UPLOAD_FOLDER, db, fileresolv
from app.models import flov, sendsmsto, store,New_store


def postnum(r):
    user= session.get("username")
    store.data[user] = New_store()
    if r.files and r.form['msg'] and r.form['num']:
        file = r.files["file"]
        filename = secure_filename(file.filename)
        if file.filename.split(".")[1] in fileresolv:
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            posts = flov(msg=r.form['msg'],file=str(os.path.join(UPLOAD_FOLDER, filename)), num=r.form['num'],user=session.get("username"))
            store.data[user](dict(numbers=posts.ress(),msg=r.form['msg'],mail=session.get("username")))
            return True
        elif r.form['msg'] and r.form['num']:
            posts = flov(msg=r.form['msg'], num=r.form['num'],user=session.get("username"))
            store.data[user](dict(numbers=posts.ress(),msg=r.form['msg'],mail=session.get("username")))
            return True
        else: return False
    elif r.form['msg'] and r.form['num']:
        posts = flov(msg=r.form['msg'], num=r.form['num'],user=session.get("username"))
        store.data[user](dict(numbers=posts.ress(),msg=r.form['msg'],mail=session.get("username")))
        return True
    elif request.files and r.form['msg']:
        file = request.files["file"]
        filename = secure_filename(file.filename)
        if file.filename.split(".")[1] in fileresolv:
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            posts = flov(msg=r.form['msg'],file=str(os.path.join(UPLOAD_FOLDER, filename)), num=r.form['num'],user=session.get("username"))
            store.data[user](dict(numbers=posts.ress(),msg=r.form['msg'],mail=session.get("username")))
            return True
    else: return False


@app.route('/index', methods=["GET", "POST"])
def index():
    if session.get('logged_in'):
        if request.method == "POST":
            if postnum(request) == True:
                return redirect("/resolv")
            else: return re_t("index.html", error=True)
        else: return re_t("index.html")
    else: redirect('/')


@app.route('/', methods=['GET', 'POST'])
def register():
    form =forms.loginf()
    if request.method == "POST":
        if db.get(request.form["mail"]) == request.form["passw"]:
            session['logged_in']=True
            session['username']= request.form["mail"]
            return redirect("/index")
        else:
            return re_t("login.html",error=True, form= form)
    else:
        return re_t("login.html", form=form)


@app.route('/resolv', methods=["GET","POST"])
def resolv():
    if session.get('logged_in'):
        data = store.data[session.get("username")].data
        if request.method == "POST":
        	sendsmsto(data["numbers"],data["msg"],session.get("username"))
            session.pop("logged_in")
            store.data.pop(session.get("username"))
            return redirect("/")
        else:
            return re_t("resolv.html",msg = data["msg"],lens=len(data["numbers"]), numbers=data["numbers"],mail=session.get("username"))
    else: return redirect('/')