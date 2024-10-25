#!/usr/bin/env python3
"""
base app
"""
import flask
import flask_babel
from typing import Union
from os import environ


class Config:
    """
    config
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = flask.Flask(__name__)
app.config.from_object(Config)
babel = flask_babel.Babel(app, locale_selector=get_locale)


@babel.localeselector
def get_locale() -> Union[str, None]:
    """
    get_locale
    """
    return flask.request.accept_languages.best_match(
        app.config["LANGUAGES"]
    )


@app.route("/", strict_slashes=False)
def home() -> flask.Response:
    """
    homepage
    """
    return flask.render_template("3-index.html")


if __name__ == "__main__":
    app.run(
        environ.get("HOST"), environ.get("PORT")
    )
