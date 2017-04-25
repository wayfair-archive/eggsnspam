from flask import Blueprint, jsonify
from .daos import BreakfastRecsDao

from eggsnspam.common.recommendations import dot_product

simple_phrasebook = Blueprint('simple_phrasebook', __name__, url_prefix='/simple_phrasebook')


@simple_phrasebook.route('/user/<int:user_id>/breakfast_recommendations', methods=["GET"])
def get_breakfast_preferences(user_id):
    """Get a person's breakfast preferences"""
    dao = BreakfastRecsDao()
    breakfasts = {}
    breakfast_scores = {}
    results = []

    # Get all the user's ingredient preferences
    user_prefs = {i['ingredient_id']: i['coefficient'] for i in dao.get_ingredient_preferences(user_id)}

    # Get all breakfasts and their ingredients
    for ingredient in dao.get_all_breakfast_ingredients():
        breakfasts.setdefault(ingredient['breakfast_id'], {})
        breakfasts[ingredient['breakfast_id']][ingredient['ingredient_id']] = ingredient['coefficient']

    # Use dot product to score similarity of breakfast ingredients and user's preferences
    for breakfast, ingredients in list(breakfasts.items()):
        breakfast_scores[breakfast] = dot_product(ingredients, user_prefs)

    # build the results object
    for breakfast in breakfasts:
        results.append({
            'breakfast_id': breakfast,
            'score': breakfast_scores[breakfast],
        })

    # sort the results by the dot product result
    results = sorted(results, reverse=True, key=lambda k: k['score'])

    return jsonify({'breakfast_recs': results})
