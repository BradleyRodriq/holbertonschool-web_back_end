#!/usr/bin/env python3
"""
basic app
"""
import flask
import flask_babel
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
babel = flask_babel.Babel(app)


@app.route("/", strict_slashes=False)
def home() -> flask.Response:
    """
    homepage
    """
    return flask.render_template("1-index.html")


if __name__ == "__main__":
    app.run(
        environ.get("HOST"), environ.get("PORT")
    )
