"""
Utility views for taking python services in and out of load balancer rotation during deployment.

NOTE: This should not stop the app from actually serving requests. This allows the load balancer to
gracefully recognize the app is being taken out of commission and take it out of rotation while
continuing to serve client requests without error.
"""

import os

from flask import current_app as APP


def healthcheck():
    """Return HTTP 200 if app is up otherwise 503."""
    status_file = APP.config['HEALTHCHECK_STATUS_FILE']

    if os.path.exists(status_file):
        return 'Not OK: current state is DOWN', 503
    else:
        return 'OK: current state is UP'


def healthcheck_up():
    """Set the app to be up."""
    status_file = APP.config['HEALTHCHECK_STATUS_FILE']

    try:
        os.remove(status_file)
    except IOError:
        pass

    return 'OK: current state is set to UP'


def healthcheck_down():
    """Set the app to be down."""
    status_file = APP.config['HEALTHCHECK_STATUS_FILE']

    # This is `touch` implemented in Python
    with open(status_file, 'a'):
        os.utime(status_file, None)

    return 'OK: current state is set to DOWN'
