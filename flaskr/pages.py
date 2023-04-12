from flask import Flask, request, render_template, redirect, session, flash, url_for, send_file
import os
from flaskr.backend import Backend
global set_app
"""This will route us to the desired location that the user chooses

In most pages a user will have a navbar where they will have specific options where they can go on the page if they are logged in or not. It will also call methods in the Backend to be able to verify information that the user has provided to either login or signup.

Typical usage example:

  return render_template('main.html')
  if logged in: return_template('upload.html')
  return redirect('login')
"""


def make_endpoints(app, back_end=False):
    instance = Backend() if back_end is False else back_end
    app.secret_key = b'0490214e639a85e4e47041cde14a56b219c0b10e709e40d9dfafe4a4e46e8807'
    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        # TODO(Checkpoint Requirement 2 of 3): Change this to use render_template
        # to render main.html on the home page.
        return render_template('main.html')

    # TODO(Project 1): Implement additional routes according to the project requirements.

    @app.route("/upload", methods=["GET", "POST"])
    def upload_file():
        if request.method == "POST":
            file = request.files['file']
            name = request.form.get('wikiname')
            instance.upload(file, name)
            return "File uploaded successfully"
        else:
            if 'user' in session:
                return render_template("upload.html")
            else:
                return redirect('login')

    @app.route("/pages/")
    def pages():
        page_names = instance.get_all_page_names()
        return render_template('pages.html', page_names=page_names)

    @app.route("/pages/<page_name>")
    def wiki_page(page_name):
        content = instance.get_wiki_page(page_name)
        return render_template('wikipage.html',
                               content=content,
                               page_name=page_name)

    @app.route("/about")
    def about_page():
        back_end = instance
        return render_template('about.html', back_end=back_end)

    @app.route('/images/<name>')
    def get_images(name):
        #tells browser this is an image
        return send_file(instance.get_image(name), mimetype='image/jpeg')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            if 'user' not in session:
                return render_template('login.html')
            else:
                flash("Already logged in!")
                return redirect('/')
        elif request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            valid = instance.sign_in(username, password)
            if valid:
                session['user'] = username
                flash("Logged Successful!", 'info')
                return redirect('/')
            else:
                flash("Incorrect Password or Username, Pleasee Try again!",
                      'error')
                return redirect('login')

    @app.route("/signup", methods=['GET', 'POST'])
    def signup():
        if request.method == 'GET':
            if 'user' not in session:
                return render_template('signup.html')
            else:
                flash("Already logged in!")
                return redirect('/')

        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            valid = instance.sign_up(username, password)
            if valid:
                flash('Account Created Successfully!')
                return redirect(url_for('login'))
            else:
                flash('Username already taken, Please try agian!', 'error')
                return redirect(url_for('signup'))

    @app.route("/logout")
    def logout():
        if 'user' not in session:
            return redirect("login")
        else:
            session.pop('user', None)
            flash("Successfully Logged out!", 'info')
            return redirect(url_for("login"))
