from wtforms import Form
from wtforms import fields
from wtforms import validators


class UserForm(Form):
    """Form for creating or updating a user."""

    first_name = fields.StringField('First Name', [validators.required()])
    last_name = fields.StringField('Last Name', [validators.required()])


class UserPreferenceForm(Form):
    """Form for creating or updating a user preference."""

    user_id = fields.IntegerField('User ID', [validators.required()])
    ingredient_id = fields.IntegerField('Ingredient ID', [validators.required()])
    coefficient = fields.FloatField('Coefficient', [validators.required()])
