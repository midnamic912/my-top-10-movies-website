from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


# create Rating Form
class RateMovieForm(FlaskForm):
    new_rating = StringField("Your Rating Out of 10 e.g.7.5", validators=[DataRequired()])
    new_review = StringField("Your Review", validators=[DataRequired()])
    submit = SubmitField("Done")


# create Adding Form
class AddMovieForm(FlaskForm):
    new_title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")
