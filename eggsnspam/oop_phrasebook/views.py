from flask import Blueprint, jsonify, request

from .collections import BreakfastCollection, IngredientCollection, UserCollection, UserPreferenceCollection
from .forms import UserForm, UserPreferenceForm
from .models import BreakfastModel, IngredientModel, UserModel, UserPreferenceModel

from eggsnspam.common import healthcheck_views
from eggsnspam.common import responses


oop_phrasebook = Blueprint('oop_phrasebook', __name__, url_prefix='/oop_phrasebook')


@oop_phrasebook.route('/breakfast/', methods=["GET"])
def list_breakfast():
    """List all breakfasts currently in the database"""
    breakfasts = BreakfastCollection()
    breakfasts.load_all()
    return jsonify(breakfasts=[x.to_dict() for x in breakfasts.models])


@oop_phrasebook.route('/breakfast/<int:breakfast_id>', methods=["GET"])
def get_breakfast(breakfast_id):
    """List all breakfasts currently in the database"""

    breakfast = BreakfastModel()
    try:
        breakfast.load_by_id(breakfast_id)
    except ValueError:
        return "Does not exist", 404
    else:
        return jsonify(breakfast.to_dict())


@oop_phrasebook.route('/ingredient/', methods=["GET"])
def list_ingredient():
    """List all ingredients currently in the database"""
    ingredients = IngredientCollection()
    ingredients.load_all()
    return jsonify(ingredients=[x.to_dict() for x in ingredients.models])


@oop_phrasebook.route('/ingredient/<int:ingredient_id>', methods=["GET"])
def get_ingredient(ingredient_id):
    """List all ingredients currently in the database"""

    ingredient = IngredientModel()
    try:
        ingredient.load_by_id(ingredient_id)
    except ValueError:
        return "Does not exist", 404
    else:
        return jsonify(ingredient.to_dict())


@oop_phrasebook.route('/user/', methods=["GET"])
def list_user():
    """List all users currently in the database"""
    users = UserCollection()
    users.load_all()
    return jsonify(users=[x.to_dict() for x in users.models])


@oop_phrasebook.route('/user/', methods=["POST"])
def create_user():
    """List all breakfasts currently in the database"""

    data = request.get_json(force=True)
    form = UserForm.from_json(data)
    if form.validate():
        new_user = UserModel()
        new_user.populate(form.data)
        new_user.save()
        return jsonify(new_user.to_dict()), 201
    else:
        return responses.invalid_request()


@oop_phrasebook.route('/user/<int:user_id>', methods=["DELETE"])
def delete_user(user_id):
    """List all breakfasts currently in the database"""

    user = UserModel()
    try:
        user.load_by_id(user_id)
    except ValueError:
        return "Does not exist", 404

    if user.delete():
        return responses.object_deleted()
    else:
        return responses.server_error()


@oop_phrasebook.route('/user/<int:user_id>', methods=["GET"])
def get_user(user_id):
    """List all breakfasts currently in the database"""

    user = UserModel()
    try:
        user.load_by_id(user_id)
    except ValueError:
        return "Does not exist", 404
    else:
        return jsonify(user.to_dict())


@oop_phrasebook.route('/user/<int:user_id>/breakfast_recommendations', methods=["GET"])
def get_user_breakfast_recs(user_id):
    """List all breakfasts currently in the database"""
    user = UserModel()
    try:
        user.load_by_id_with_preferences(user_id)
    except ValueError:
        return "Does not exist", 404

    return jsonify({'breakfast_recs': user.get_recommendations()})


@oop_phrasebook.route('/user/<int:user_id>', methods=["PUT"])
def update_user(user_id):
    """Update a breakfast"""

    user = UserModel()
    try:
        user.load_by_id(user_id)
    except ValueError:
        return "Does not exist", 404

    form = UserForm.from_json(request.get_json(force=True), user)
    if form.validate():
        user.populate(form.data)
        user.save()
        return jsonify(user.to_dict())
    else:
        return responses.invalid_request()


@oop_phrasebook.route('/user/<int:user_id>/preference/', methods=["GET"])
def list_user_preferences(user_id):
    """List all user preferences currently in the database"""

    user = UserModel()
    try:
        user.load_by_id(user_id)
    except ValueError:
        return "Does not exist", 404

    prefs = UserPreferenceCollection()
    prefs.load_all_for_user(user.id)

    return jsonify({'user_preferences': [p.to_dict() for p in prefs.models]})


@oop_phrasebook.route('/user/<int:user_id>/preference/', methods=["POST"])
def create_user_preferences(user_id):
    """Create a new user record"""

    user = UserModel()
    try:
        user.load_by_id(user_id)
    except ValueError:
        return "Does not exist", 404

    data = request.get_json(force=True)
    data['user_id'] = user.id

    form = UserPreferenceForm.from_json(data)
    if form.validate():
        new_pref = UserPreferenceModel()
        new_pref.populate(form.data)
        new_pref.save()
        return jsonify(new_pref.to_dict()), 201
    else:
        return responses.invalid_request()

    return jsonify({})


@oop_phrasebook.route('/user/<int:user_id>/preference/<int:ingredient_id>', methods=["GET"])
def get_user_preference(user_id, ingredient_id):
    """List all breakfasts currently in the database"""
    pref = UserPreferenceModel()
    try:
        pref.load_by_user_ingredient(user_id, ingredient_id)
    except ValueError:
        return "Does not exist", 404
    else:
        return jsonify(pref.to_dict())


@oop_phrasebook.route('/user/<int:user_id>/preference/<int:ingredient_id>', methods=["PUT"])
def update_user_preference(user_id, ingredient_id):
    """Update a breakfast"""
    pref = UserPreferenceModel()
    try:
        pref.load_by_user_ingredient(user_id, ingredient_id)
    except ValueError:
        return "Does not exist", 404

    form = UserPreferenceForm.from_json(request.get_json(force=True), pref)
    if form.validate():
        pref.populate(form.data)
        pref.save()
        return jsonify(pref.to_dict())
    else:
        return responses.invalid_request()


@oop_phrasebook.route('/user/<int:user_id>/preference/<int:ingredient_id>', methods=["DELETE"])
def delete_user_preference(user_id, ingredient_id):
    """Delete a user record from the database"""
    pref = UserPreferenceModel()
    try:
        pref.load_by_user_ingredient(user_id, ingredient_id)
    except ValueError:
        return "Does not exist", 404

    if pref.delete():
        return responses.object_deleted()
    else:
        return responses.server_error()

# Add healthcheck endpoints
oop_phrasebook.add_url_rule('/healthcheck', view_func=healthcheck_views.healthcheck)
oop_phrasebook.add_url_rule('/healthcheck/up', view_func=healthcheck_views.healthcheck_up)
oop_phrasebook.add_url_rule('/healthcheck/down', view_func=healthcheck_views.healthcheck_down)
