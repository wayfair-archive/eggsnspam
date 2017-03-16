"""
HTTP response helper functions.

If you find yourself re-defining the same typesof responses in multiple places, it's better
to define them in functions and re-use them across your views.
"""

from flask import jsonify


def invalid_request(error_message="Invalid Request"):
    """Return an Invalid Request response, and include a (hopefully) helpful error message."""
    response = jsonify({"error": error_message})
    response.status_code = 400
    return response


def object_deleted():
    """The object was succesfully deleted"""
    response = jsonify({})
    response.status_code = 204
    return response


def server_error(error_message="Server Error"):
    """Return an Invalid Request response, and include a (hopefully) helpful error message."""
    response = jsonify({"error": error_message})
    response.status_code = 500
    return response
