#!/usr/bin/env python3
"""
basic app
"""
from typing import Union
from os import environ
import flask
import flask_babel
import babel



class Config:
    """
    babel config
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = flask.Flask(__name__)
app.config.from_object(Config)



@babel.localeselector
def get_locale() -> Union[str, None]:
    """
    get_locale
    """
    locale_arg: Union[str, None] = flask.request.args.get("locale", None)

    if locale_arg is not None and locale_arg in app.config["LANGUAGES"]:
        return locale_arg

    return flask.request.accept_languages.best_match(
        app.config["LANGUAGES"]
    )

babel = flask_babel.Babel(app, locale_selector=get_locale)

@app.route("/", strict_slashes=False)
def home() -> flask.Response:
    """
    homepage
    """
    return flask.render_template("4-index.html")


if __name__ == "__main__":
    app.run(
        environ.get("HOST"), environ.get("PORT")
    )
