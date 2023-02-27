from flask import Flask
from flask import render_template
from flask import request
from .backend import *

def make_endpoints(app):
    backend = Backend()

    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        # TODO(Checkpoint Requirement 2 of 3): Change this to use render_template
        # to render main.html on the home page.
        return render_template('main.html')


    # TODO(Project 1): Implement additional routes according to the project requirements.

    @app.route("/sign_up", methods=['GET', 'POST'])
    def signup():
        if request.method == 'GET':
            # Return the HTML page
            return render_template("signup.html")
        
        if request.method == 'POST':
            # Take in the username and password then redirect them to the sign in page
            # Get type in answers and call the backend to add them to the sheet
            username = request.form['username']
            password = request.form['password']
            valid = backend.sign_up(username, password)

            return render_template("signup.html", valid=valid)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        
        if request.method == 'POST':
            pass