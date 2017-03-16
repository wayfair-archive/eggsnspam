from wtforms import Form
from wtforms import fields
from wtforms import validators


class UserForm(Form):
    """Form for creating or updating a user."""

    first_name = fields.StringField(u'First Name', [validators.required()])
    last_name = fields.StringField(u'Last Name', [validators.required()])


class UserPreferenceForm(Form):
    """Form for creating or updating a user preference."""

    user_id = fields.IntegerField(u'User ID', [validators.required()])
    ingredient_id = fields.IntegerField(u'Ingredient ID', [validators.required()])
    coefficient = fields.FloatField(u'Coefficient', [validators.required()])
