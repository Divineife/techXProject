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
            category = request.form['category']
            instance.upload(file, name, category)
            return redirect('pages')
        else:
            if 'user' in session:
                categories = instance.get_categories()
                return render_template("upload.html", categories=categories)
            else:
                return redirect('login')

    @app.route("/pages/")
    def pages():
        """
        This route is the endpoint to display all pages
        The list of page names uploaded is passed to the html template
        """
        page_names = instance.get_all_page_names()
        return render_template('pages.html', page_names=page_names)

    @app.route("/pages/<page_name>", methods=['GET', 'POST'])
    def wiki_page(page_name):
        """
        This route is the endpoint for each specific page
        The content of the webpage is passed as content and the pagename is passed as page_name
        The status of the user i.e if he is the author of the page is passed as the boolean authored
        """
        content = instance.get_wiki_page(page_name)
        if request.method == 'POST':
            username = session['user']
            #this is a json object
            pages_comments = instance.get_commentbucket()
            comment = request.form.get('user_comment')
            if page_name not in pages_comments:
                pages_comments[page_name] = {username: [comment]}
            elif username in pages_comments[page_name]:
                comments_inpage = pages_comments[page_name]
                comments_inpage[username].append(comment)
            else:
                comments_inpage = pages_comments[page_name]
                comments_inpage[username] = [comment]
            instance.add_comment(pages_comments)
            return redirect(f"/pages/{page_name}")

        elif request.method == 'GET':
            page_username = instance.get_author(page_name)
            authorized = instance.check_user(page_name, page_username)
            page_category = instance.get_page_category(page_name)
            pages_comments = instance.get_commentbucket()
            print(request.method)
            if page_name not in pages_comments:
                pages_comments[page_name] = {}
            comments_inpage = pages_comments[page_name]
            return render_template('wikipage.html',
                                   content=content,
                                   page_name=page_name,
                                   authored=authorized,
                                   page_category=page_category,
                                   comments_inpage=comments_inpage)

    @app.route("/delete/page", methods=["GET", "POST"])
    def delete():
        """
        This is the endpoint to delete a wiki-page
        """
        page_name = request.form.get('page_name')
        if 'user' not in session:
            return redirect("login")
        else:
            if instance.delete(page_name):
                return redirect("/pages/")
            else:
                flash("You are not authorized to delete this page")

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
                flash("Logged In Successfully!", 'info')
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

    @app.route("/pages/<page_name>/edit", methods=["GET", "POST"])
    def edit_wiki_page(page_name):
        if request.method == "POST":
            new_content = request.form.get("new_content")
            name = request.form.get("page_name")
            instance.edit_wiki_page(page_name, new_content, name)
            return redirect(url_for("wiki_page", page_name=page_name))
        else:
            if "user" in session:
                content = instance.get_wiki_page(page_name)
                # return redirect(url_for("wiki_page", page_name=page_name))
                return render_template("wikipage.html",
                                       page_name=page_name,
                                       content=content)
            else:
                return redirect(url_for("login"))
