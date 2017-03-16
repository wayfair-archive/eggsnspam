from flask import Blueprint, jsonify, request

from sqlalchemy.orm import load_only, joinedload
from sqlalchemy.exc import IntegrityError

from .forms import UserForm, UserPreferenceForm, UserPreferenceUpdateForm
from .models import Breakfast, Ingredient, User, UserPreference

from eggsnspam.common import healthcheck_views
from eggsnspam.common import responses
from eggsnspam.extensions import db


oop_orm = Blueprint('oop_orm', __name__, url_prefix='/oop_orm')


@oop_orm.route('/breakfast/', methods=["GET"])
def list_breakfasts():
    """List all breakfasts currently in the database"""
    breakfasts = Breakfast.query.with_hint(Breakfast, "WITH (NOLOCK)").options(load_only("id")).all()
    return jsonify(breakfasts=[{"id": x.id} for x in breakfasts])


@oop_orm.route('/breakfast/<int:breakfast_id>', methods=["GET"])
def get_breakfast(breakfast_id):
    """Get a breakfast by its primary key"""
    breakfast = Breakfast.query.with_hint(Breakfast, "WITH (NOLOCK)").get(breakfast_id)
    if breakfast:
        return jsonify(breakfast.to_dict())
    else:
        return "Does not exist", 404


@oop_orm.route('/ingredient/', methods=["GET"])
def list_ingredients():
    """List all ingredients currently in the database"""
    ingredients = Ingredient.query.with_hint(Ingredient, "WITH (NOLOCK)").options(load_only("id")).all()
    return jsonify(ingredients=[{"id": x.id} for x in ingredients])


@oop_orm.route('/ingredient/<int:ingredient_id>', methods=["GET"])
def get_ingredient(ingredient_id):
    """Get a ingredient by its primary key"""
    ingredient = Ingredient.query.with_hint(Ingredient, "WITH (NOLOCK)").get(ingredient_id)
    if ingredient:
        return jsonify(ingredient.to_dict())
    else:
        return "Does not exist", 404


@oop_orm.route('/user/', methods=["GET"])
def list_user():
    """List all users currently in the database"""
    users = User.query.with_hint(User, "WITH (NOLOCK)").all()
    return jsonify(users=[x.to_dict() for x in users])


@oop_orm.route('/user/', methods=["POST"])
def create_user():
    """Create a new user record"""
    data = request.get_json(force=True)
    form = UserForm.from_json(data)
    if form.validate():
        new_user = User(**form.data)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201
    else:
        return responses.invalid_request()


@oop_orm.route('/user/<int:user_id>', methods=["DELETE"])
def delete_user(user_id):
    """Delete a user record from the database"""
    user = User.query.with_hint(User, "WITH (NOLOCK)").get(user_id)

    if not user:
        return "Does not exist", 404

    db.session.delete(user)
    db.session.commit()
    return responses.object_deleted()


@oop_orm.route('/user/<int:user_id>', methods=["GET"])
def get_user(user_id):
    """List all breakfasts currently in the database"""
    user = User.query.with_hint(User, "WITH (NOLOCK)").get(user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        return "Does not exist", 404


@oop_orm.route('/user/<int:user_id>/breakfast_recommendations', methods=["GET"])
def get_user_breakfast_recs(user_id):
    """List all breakfasts currently in the database"""
    user = User.query.options(joinedload('preferences')).with_hint(User, "WITH (NOLOCK)").filter_by(id=user_id).one()
    if not user:
        return "Does not exist", 404
    return jsonify({'breakfast_recs': user.get_recommendations()})


@oop_orm.route('/user/<int:user_id>', methods=["PUT"])
def update_user(user_id):
    """Update a breakfast"""
    user = User.query.with_hint(User, "WITH (NOLOCK)").get(user_id)
    if user:
        form = UserForm.from_json(request.get_json(force=True), user)
        if form.validate():
            form.populate_obj(user)
            db.session.add(user)
            db.session.commit()
            return jsonify(user.to_dict())
        else:
            return responses.invalid_request()
    else:
        return "Does not exist", 404


@oop_orm.route('/user/<int:user_id>/preference/', methods=["GET"])
def list_user_preferences(user_id):
    """List all user preferences currently in the database"""
    user = User.query.with_hint(User, "WITH (NOLOCK)").get(user_id)

    if not user:
        return "Does not exist", 404

    user_preferences = UserPreference.query.filter_by(user_id=user.id).with_hint(UserPreference, "WITH (NOLOCK)").all()
    return jsonify(user_preferences=[pref.to_dict() for pref in user_preferences])


@oop_orm.route('/user/<int:user_id>/preference/', methods=["POST"])
def create_user_preferences(user_id):
    """Create a new user record"""
    user = User.query.with_hint(User, "WITH (NOLOCK)").get(user_id)

    if not user:
        return "Does not exist", 404

    data = request.get_json(force=True)

    # set the user_id to the one being passed in
    data['user'] = user.id

    form = UserPreferenceForm.from_json(data)
    if form.validate():
        new_user_preference = UserPreference(**form.data)
        db.session.add(new_user_preference)
        try:
            db.session.commit()
        except IntegrityError:
            # Attempted to create a duplicate user/ingredient relationship
            return responses.invalid_request()
        else:
            return jsonify(new_user_preference.to_dict()), 201
    return responses.invalid_request()


@oop_orm.route('/user/<int:user_id>/preference/<int:ingredient_id>', methods=["GET"])
def get_user_preference(user_id, ingredient_id):
    """List all breakfasts currently in the database"""
    user_preference = UserPreference.query.get((user_id, ingredient_id))

    if user_preference:
        return jsonify(user_preference.to_dict())
    else:
        return "Does not exist", 404


@oop_orm.route('/user/<int:user_id>/preference/<int:ingredient_id>', methods=["PUT"])
def update_user_preference(user_id, ingredient_id):
    """Update a breakfast"""
    user_preference = UserPreference.query.get((user_id, ingredient_id))
    if user_preference:
        form = UserPreferenceUpdateForm.from_json(request.get_json(force=True), user_preference)
        if form.validate():
            form.populate_obj(user_preference)
            db.session.add(user_preference)
            db.session.commit()
            return jsonify(user_preference.to_dict())
        else:
            return responses.invalid_request()
    else:
        return "Does not exist", 404


@oop_orm.route('/user/<int:user_id>/preference/<int:ingredient_id>', methods=["DELETE"])
def delete_user_preference(user_id, ingredient_id):
    """Delete a user record from the database"""
    user_preference = UserPreference.query.get((user_id, ingredient_id))

    if not user_preference:
        return "Does not exist", 404

    db.session.delete(user_preference)
    db.session.commit()
    return responses.object_deleted()


# Add healthcheck endpoints
oop_orm.add_url_rule('/healthcheck', view_func=healthcheck_views.healthcheck)
oop_orm.add_url_rule('/healthcheck/up', view_func=healthcheck_views.healthcheck_up)
oop_orm.add_url_rule('/healthcheck/down', view_func=healthcheck_views.healthcheck_down)
