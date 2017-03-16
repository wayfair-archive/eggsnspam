#!/bin/bash
env FLASK_CONFIG='eggsnspam.settings.test.TestingConfig' python -m unittest discover
