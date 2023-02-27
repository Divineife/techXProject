from flask import Flask, request, render_template
import os
from flaskr.backend import Backend


def make_endpoints(app):

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
            print(request)
            file = request.files['file']
            upload_instance = Backend()
            upload_instance.upload(file)
            return "File uploaded successfully"
        else:
            return render_template("upload.html")

