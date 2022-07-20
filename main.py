from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from form import RateMovieForm, AddMovieForm
import requests, os

# set env vars
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
API_TOKEN = os.getenv('API_TOKEN')
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

# app init
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
Bootstrap(app)


# create a database
app.config[
    'SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# create a table
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    rating = db.Column(db.Float)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String(1000))
    img_url = db.Column(db.String(1000), nullable=False)


db.create_all()


@app.route("/")
def home():
    # make the db ordered by column field 'rating'
    movies = Movie.query.order_by("rating")

    # create a ranking num list according to the db entries amount
    # reverse the ranking num because we want the best ranking is the last one
    list_of_ranking = [int for int in range(1, Movie.query.count() + 1)][::-1]

    # update ranking value to the movies in db
    index = 0
    for movie in movies:
        movie.ranking = list_of_ranking[index]
        db.session.commit()
        index += 1
    return render_template("index.html", movies=movies)


@app.route("/edit", methods=["GET", "POST"])
def edit():
    form = RateMovieForm()
    movie_id = request.args.get("id")
    movie_to_update = Movie.query.get(movie_id)
    # create a Rating Updating Form
    if request.method != "POST":
        return render_template("edit.html", form=form, movie=movie_to_update)

    # if the form be submitted
    if form.validate_on_submit():
        new_rating = request.form["new_rating"]
        new_review = request.form["new_review"]
        movie_to_update.rating = new_rating
        movie_to_update.review = new_review
        db.session.commit()
        return redirect(url_for('home'))


@app.route("/delete")
def delete():
    movie_id = request.args.get("id")
    movie_to_delete = Movie.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddMovieForm()
    if form.validate_on_submit():
        # search movies with keywords from TMDB
        title = request.form["new_title"]
        headers = {"Authorization": f'Bearer {API_TOKEN}'}
        url = "https://api.themoviedb.org/3/search/movie"
        params = {"query": title, }
        response = requests.get(url=url, params=params, headers=headers)
        results = response.json()["results"]
        return render_template("select.html", results=results)

    return render_template("add.html", form=form)


@app.route("/get_movie_data_and_add")
def get_movie_data_and_add():
    # get movie data from TMDB
    headers = {"Authorization": f'Bearer {API_TOKEN}'}
    movie_id = request.args.get("id")
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    response = requests.get(url, headers=headers)
    data = response.json()

    # create new movie
    new_movie = Movie(
        title=data["title"],
        year=data["release_date"].split("-")[0],
        description=data["overview"],
        img_url=''.join(["https://image.tmdb.org/t/p/w500", data["poster_path"]])
    )
    db.session.add(new_movie)
    db.session.commit()

    movie_id_in_db = Movie.query.filter_by(title=data["title"]).first().id
    return redirect(url_for("edit", id=movie_id_in_db))


if __name__ == '__main__':
    app.run(debug=True)
