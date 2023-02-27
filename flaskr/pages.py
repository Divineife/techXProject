from flask import Flask, request, render_template
import os
from flaskr.backend import Backend


def make_endpoints(app):
    instance = Backend()

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
            instance.upload(file,name)
            return "File uploaded successfully"
        else:
            return render_template("upload.html")

    @app.route("/pages/")
    def pages():
        page_names = instance.get_all_page_names()
        return render_template('pages.html', page_names = page_names)

    @app.route("/login")
    def login():
        return render_template('login.html')

    @app.route("/signUp")
    def signup():
        return render_template('signup.html')

    @app.route("/pages/<page_name>")
    def wiki_page(page_name):
        content = instance.get_wiki_page(page_name)
        return render_template('wikipage.html', content = content, page_name= page_name)

