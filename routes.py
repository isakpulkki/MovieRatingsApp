from app import app
from flask import abort, render_template, request, redirect
import users
import movies
import reviews
import genres
import requests

@app.route("/")
def index():
    if request.method == "GET":
        if result := movies.get_all():
            return render_template("index.html", movies=result)
        return render_template("error.html", message="Movies have not been added yet")


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        query = request.args["query"]
        if result := movies.search(query):
            return render_template("movies.html", movies=result, genres=genres.get())
        return render_template("error.html", message="Your search did not match any results")


@app.route("/user", methods=["GET", "POST"])
def get_user():
    if request.method == "GET":
        if (users.get_user_id()):
            return render_template("user.html")
        return render_template("error.html", message="You are not logged in")


@app.route("/movies", methods=["GET", "POST"])
def get_movies():
    if request.method == "GET":
        if result := movies.get_all():
            return render_template("movies.html", movies=result, genres=genres.get_genres())
        return render_template("error.html", message="Movies have not been added yet")
    if request.method == "POST":
        genreid = request.form["genre"]
        if genreid == "all":
            return render_template("movies.html", movies=movies.get_all(), genres=genres.get_genres())
        if result := movies.get_genre(genreid):
            return render_template("movies.html", movies=result, genres=genres.get_genres(), selected=int(genreid))
        return render_template("error.html", message="This genre does not have movies yet")


@app.route("/requests/<int:movieid>", methods=["POST"])
def approve_requests(movieid):
    if request.method == "POST":
        if users.get_admin():
            if 'add' in request.form:
                requests.delete(movieid)
            elif 'delete' in request.form:
                requests.delete(movieid)
                delete_movie(movieid)
            return redirect("/requests")
        return render_template("error.html", message="You don't have access to this page")


@app.route("/requests", methods=["GET", "POST"])
def get_requests():
    if request.method == "GET":
        if users.get_admin():
            return (render_template("requests.html", movies=result)
                    if (result := movies.get_requested())
                    else render_template(
                    "error.html", message="Movies have not been requested yet"))
        else:
            return render_template("error.html", message="You don't have access to this page")


@app.route("/request", methods=["GET", "POST"])
def request_movie():
    if not users.get_user_id():
        return render_template("error.html", message="You must be logged in to request new movies")
    if len(requests.get_user_request()) >= 3:
        return render_template("error.html", message="You have already requested three movies, wait \
                                until they are accepted to request a new one")
    if request.method == "GET":
        return render_template("request.html", genres=genres.get())
    if request.method == "POST":
        if users.check_csrf() != request.form["csrf_token"]:
            abort(403)
        cover = request.files['cover']
        name = request.form["name"]
        genre = request.form["genre"]
        description = request.form["description"]
        if not cover or not description or not name:
            return render_template("error.html", message="Movie needs name, description and cover photo")
        if len(description) > 980 or len(name) > 180:
            return render_template("error.html", message="Your name or description is too long")
        if cover.filename.endswith('.jpg') or cover.filename.endswith('.png') or cover.filename.endswith('.jpeg'):
            data = cover.read()
            if users.get_admin():
                if not movies.add(name, description, data, genre):
                    return render_template("error.html", message="Something went wrong")
            elif not requests.add(movies.add(name, description, data, genre)):
                return render_template("error.html", message="Something went wrong")
            return redirect("/request")
        return render_template("error.html", message="Cover photo needs to be in .jpg or .png filetype")


@app.route("/add", methods=["GET", "POST"])
def add_movie():
    if users.get_admin() and request.method == "GET":
        return render_template("request.html", genres=genres.get())
    return render_template("error.html", message="You don't have access to this page")


@app.route("/delete/<int:movieid>", methods=["POST"])
def delete_movie(movieid):
    if request.method == "POST":
        if users.check_csrf() != request.form["csrf_token"]:
            abort(403)
        if (users.get_admin()) and movies.delete(movieid):
            return redirect("/movies")
        return render_template("error.html", message="Something went wrong")


@app.route("/cover/<int:id>", methods=["GET", "POST"])
def get_cover(id):
    if request.method == "GET":
        cover = movies.get_cover(id)
        return (
            cover or render_template(
                "error.html", message="This cover does not exist"))


@app.route("/movies/<int:id>", methods=["GET", "POST"])
def get_movie(id):
    if request.method == "GET":
        if movies.get_one(id):
            return render_template("movie.html", movie=movies.get_one(id),
                        reviews=reviews.get_movie_reviews(id), review=reviews.get_user_review(id))
        return render_template("error.html", message="This movie does not exist")


@app.route("/movies/<int:movieid>/reviews/", methods=["POST"])
def add_review(movieid):
    if request.method == "POST":
        if users.check_csrf() != request.form["csrf_token"]:
            abort(403)
        userid = users.get_user_id()
        if userid:
            if reviews.get_user_review(movieid):
                return render_template("error.html", message="You have already reviewed this movie")
            if requests.get_movie_request(movieid):
                return render_template("error.html", message="This movie is still being requested")
            description = request.form["description"]
            stars = int(request.form["rate"])
            if not stars:
                return render_template("error.html", message="Something went wrong, did you select rating?")
            if len(description) > 780:
                return render_template("error.html", message="Review description should be less than \
                                       780 characters")
            if stars < 1 or stars > 5 or not reviews.add(description, stars, movieid):
                return render_template("error.html", message="Something went wrong")
            return redirect("/movies/" + str(movieid))
        return render_template("error.html", message="Are you sure your logged in?")


@app.route("/movies/<int:movieid>/reviews/delete/<int:reviewid>", methods=["POST"])
def delete_review(movieid, reviewid):
    if users.check_csrf() != request.form["csrf_token"]:
        abort(403)
    if request.method == "POST":
        if reviews.delete(reviewid):
            return redirect(f"/movies/{str(movieid)}")
        return render_template("error.html", message="Something went wrong")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        success, value = users.login(username, password)
        if not success:
            if value == 'user':
                return render_template("error.html", message="No account found with such username")
            if value == 'password':
                return render_template("error.html", message="You did not enter valid password")
        return redirect("/")


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        if users.username_available(username):
            return render_template("error.html", message="Username already taken, try another one")
        if len(username) < 3 or len(username) > 16:
            return render_template("error.html", message="Your username should contain 3-16 characters")
        password = request.form["password"]
        password2 = request.form["password2"]
        if password != password2:
            return render_template("error.html", message="Your password's are not the same")
        if len(password) < 5 or len(username) > 24:
            return render_template("error.html", message="Your password should contain 5-24 characters")
        if not users.register(username, password):
            return render_template("error.html", message="Register failed")
        users.login(username, password)
        return redirect("/")


@app.route("/password", methods=["POST"])
def change_password():
    if request.method == "POST":
        if users.get_admin():
            return render_template("error.html", message="Admin's password can't be changed this way")
        if users.get_user_id():
            if users.check_csrf() != request.form["csrf_token"]:
                abort(403)
            oldpassword = request.form["oldpassword"]
            password = request.form["password"]
            password2 = request.form["password2"]
            if not password == password2:
                return render_template("error.html", message="Your password's are not the same")
            if users.change_password(oldpassword, password):
                return redirect("/")
            return render_template("error.html", message="Something went wrong, did you \
                                   select correct old password?")


@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(405)
def handle_error(error):
    messages = {
        403: "Something went wrong",
        404: "The page you are trying to reach does not exist",
        405: "The method is not allowed for the requested URL"}
    return render_template('error.html', message=messages.get(error.code))
