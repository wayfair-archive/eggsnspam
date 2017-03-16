from flask import Blueprint, Response


home = Blueprint('home', __name__, url_prefix='/')


@home.route('/', methods=["GET"])
def index():
    """Send a string to let the user know the service is running"""
    return Response("Hello world! You're up and running with Eggs'N'Spam.", status=200, mimetype="text/plain")
