#!/usr/bin/env python3
"""
2-app.py
"""
import flask
import flask_babel
from typing import Union
from os import environ


class Config:
    """
    Contains the allowed languages
    and default timezone for 'babel'.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = flask.Flask(__name__)
app.config.from_object(Config)
babel = flask_babel.Babel(app)


@babel.localeselector
def get_locale() -> Union[str, None]:
    """
    get locale
    """
    return flask.request.accept_languages.best_match(
        app.config["LANGUAGES"]
    )


@app.route("/", strict_slashes=False)
def home() -> flask.Response:
    """
    homepage
    """
    return flask.render_template("2-index.html")


if __name__ == "__main__":
    app.run(
        environ.get("HOST"), environ.get("PORT")
    )
