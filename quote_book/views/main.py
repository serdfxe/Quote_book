from configparser import MAX_INTERPOLATION_DEPTH
from flask import Blueprint, redirect, render_template, request, session, url_for
from quote_book.config import *
from quote_book.models import Quote_book_db, User_db


main = Blueprint("main", __name__)


@main.route("/", methods=('GET', 'POST'))
def root_page():
    return redirect(url_for("main.searching_page"))


@main.route("/home", methods=('GET', 'POST'))
def home_page():
    if request.method == "GET":
        name = session.get("name")
        if name == None:
            return redirect("reg")
        return render_template(urls["home"], navbar = navbar_body, nav_style = navbar_style, name = session['name'], urls = urls_navbar)
        
    if request.method == "POST":
        if request.form["action"] == "quit":
            session.pop("name")
            print(session.get("name"))
            print("OK LET'S GO")
            return redirect(url_for('main.registration_page'))


@main.route("/search", methods=('GET', 'POST'))
def searching_page():
    if request.method == "GET":
        return render_template(urls["search"], navbar = navbar_body, nav_style = navbar_style, results={})
    
    if request.method == "POST":
        name = session.get("name")
        if request.form["action"] == "search":
            query = request.form['query']
            return render_template(urls["search"], navbar = navbar_body, nav_style = navbar_style, results=Quote_book_db.search_quotes(query), likes= User_db.get_user_list(name), query = query)
        
        elif request.form["action"] == "add":
            if name == None: return redirect(url_for("main.registration_page"))
            User_db.add_quote_to_user_list(name, int(request.form["quoteID"]))
            query = request.form['query']
            return render_template(urls["search"], navbar = navbar_body, nav_style = navbar_style, results=Quote_book_db.search_quotes(query), likes= User_db.get_user_list(name), query = query)
        
        elif request.form["action"] == "remove":
            if name == None: return redirect(url_for("main.registration_page"))
            quoteID = request.form["quoteID"]
            query = request.form["query"]
            User_db.remove_quote_from_user_list(name, quoteID)
            return render_template(urls["search"], navbar = navbar_body, nav_style = navbar_style, results=Quote_book_db.search_quotes(query), likes= User_db.get_user_list(name), query = query)


@main.route("/reg", methods=('GET', 'POST'))
def registration_page():
    if request.method == "GET":
        return render_template(urls['reg'], navbar = navbar_body, nav_style = navbar_style, method = "get", urls = urls_navbar)

    if request.method == "POST":
        is_correct = User_db.add_user_to_db(request.form['name'], request.form['password'], [])
        if is_correct: session["name"] = request.form['name']
        return render_template(urls['reg'], navbar = navbar_body, nav_style = navbar_style, method = "post", is_correct = is_correct, urls = urls_navbar)


@main.route("/log", methods=('GET', 'POST'))
def login_page():
    if request.method == "GET":
        return render_template(urls['log'], navbar = navbar_body, nav_style = navbar_style, method = "get", urls = urls_navbar)

    if request.method == "POST":
        is_correct = User_db.check_password(request.form['name'], request.form['password'])
        if is_correct: session["name"] = request.form['name']
        return render_template(urls['log'], navbar = navbar_body, nav_style = navbar_style, method = "post", is_correct = is_correct, urls = urls_navbar)


@main.route("/saves", methods=('GET', 'POST'))
def saves_page():
    name = session.get("name")
    if name == None: return redirect(url_for("main.registration_page"))

    if request.method == "GET":
        results=Quote_book_db.get_quotes_from_user_list(name)

        return render_template(urls["saves"], urls = urls_navbar, navbar = navbar_body, nav_style = navbar_style, results=results, name = name)
    
    if request.method == "POST":
        if request.form["action"] == "remove":
            quoteID = request.form["quoteID"]
            User_db.remove_quote_from_user_list(name, quoteID)
            results=Quote_book_db.get_quotes_from_user_list(name)
            return render_template(urls["saves"], urls = urls_navbar, navbar = navbar_body, nav_style = navbar_style, results=results, name = name)
