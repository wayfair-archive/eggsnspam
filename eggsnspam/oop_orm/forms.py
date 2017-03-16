"""
Declare forms so you can validate user input.

Not only is it more expressive than a bunch of conditionals, it's much more secure.
"""

from wtforms import Form
from wtforms.ext.sqlalchemy.orm import model_form

from .models import User, UserPreference

from ..extensions import db

# Automatically define validation class by inspecting the User class
UserForm = model_form(User, base_class=Form, exclude=('preferences',))

# Automatically define validation class by inspecting the User class
UserPreferenceForm = model_form(UserPreference, base_class=Form, db_session=db.session)

# Automatically define validation class by inspecting the User class
UserPreferenceUpdateForm = model_form(UserPreference,
                                      base_class=Form,
                                      db_session=db.session,
                                      exclude=('user', 'ingredient'))
