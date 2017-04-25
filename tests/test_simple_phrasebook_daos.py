from . import BaseTestCase
from .mixins import PhrasebookFixturedTestCase
from eggsnspam.simple_phrasebook.daos import BreakfastRecsDao


class BreakfastRecsDaoTestCase(PhrasebookFixturedTestCase, BaseTestCase):

    def setUp(self):
        super(BreakfastRecsDaoTestCase, self).setUp()
        self.dao = BreakfastRecsDao()

    def test_get_ingredient_preferences(self):
        """It gets a user's ingredient preferences"""
        prefs = self.dao.get_ingredient_preferences(1)
        self.assertEqual(len(prefs), 3)
        self.assertTrue('coefficient' in list(prefs[0].keys()))
        self.assertTrue('ingredient_id' in list(prefs[0].keys()))

    def test_get_all_breakfast_ingredients(self):
        """It gets all breakfasts for all ingredients"""
        ingredients = self.dao.get_all_breakfast_ingredients()
        self.assertEqual(len(ingredients), 9)
        self.assertTrue('coefficient' in list(ingredients[0].keys()))
        self.assertTrue('ingredient_id' in list(ingredients[0].keys()))
        self.assertTrue('breakfast_id' in list(ingredients[0].keys()))
