#!/usr/bin/env python3
"""
basic app
"""
import flask
import flask_babel
from typing import Union
from os import environ


class Config:
    """
    language and babel config
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
        host=environ.get("HOST", "0.0.0.0"),
        port=int(environ.get("PORT", 5000))
    )
