from .factories.oop_orm_factories import (BreakfastFactory, IngredientFactory, UserFactory,
                                         UserPreferenceFactory, BreakfastIngredientFactory)

from eggsnspam.extensions import db

from . import BaseTestCase
from .mixins import OrmTestCase


class UserTestCase(OrmTestCase, BaseTestCase):

    def test_full_name(self):
        """It returns a person's full name"""
        user = UserFactory.build(first_name='Adam', last_name='Anderson')
        self.assertEqual(user.full_name, 'Adam Anderson')

    def test_to_dict(self):
        """It serlializes as a dict representation"""
        user_props = {'id': 1, 'first_name': 'Karma', 'last_name': 'Kabana'}
        user = UserFactory.build(**user_props)
        self.assertDictEqual(user.to_dict(), user_props)

    def test_get_recommendations(self):
        """It gets recommended breakfasts"""
        user = UserFactory.create(first_name='Adam', last_name='Anderson')

        self.assertEqual(user.get_recommendations(), [])

        # expect a breakfast with no ingredients to be excluded included
        breakfast = BreakfastFactory.create()
        self.assertEqual(user.get_recommendations(), [])

        # expect a single recommendation with no breakfasts
        ingredient = IngredientFactory.create()
        BreakfastIngredientFactory(breakfast=breakfast,
                                   ingredient=ingredient,
                                   coefficient=1)
        self.assertEqual(len(user.get_recommendations()), 1)
        self.assertDictEqual(user.get_recommendations()[0], {'breakfast_id': breakfast.id, 'score': 0.0})

        # expect a single recommendation with no breakfasts
        UserPreferenceFactory.create(user=user,
                                     ingredient=ingredient,
                                     coefficient=1)
        self.assertEqual(len(user.get_recommendations()), 1)
        self.assertDictEqual(user.get_recommendations()[0], {'breakfast_id': breakfast.id, 'score': 1})

        # expect a second breakfast with less relvency to show up in recommendations position #2
        breakfast_2 = BreakfastFactory.create()
        BreakfastIngredientFactory(breakfast=breakfast_2,
                                   ingredient=ingredient,
                                   coefficient=0.1)
        self.assertEqual(len(user.get_recommendations()), 2)
        self.assertDictEqual(user.get_recommendations()[0], {'breakfast_id': breakfast.id, 'score': 1})
        self.assertDictEqual(user.get_recommendations()[1], {'breakfast_id': breakfast_2.id, 'score': 0.1})


class UserPreferenceTestCase(OrmTestCase, BaseTestCase):

    def test_to_dict(self):
        """It serlializes as a dict representation"""
        user = UserFactory(first_name='Adam', last_name='Anderson')
        ingredient = IngredientFactory(name='Spam')
        user_preference = UserPreferenceFactory.create(user=user, ingredient=ingredient)

        # Force the session to flush. Otherwise I wasn't getting IDs for child objects
        db.session.flush()

        self.assertDictEqual(user_preference.to_dict(), {'user_id': user.id,
                                                         'ingredient_id': ingredient.id,
                                                         'coefficient': user_preference.coefficient})


class BreakfastTestCase(OrmTestCase, BaseTestCase):

    def test_full_name(self):
        """It returns a person's full name"""
        user = UserFactory.build(first_name='Adam', last_name='Anderson')
        self.assertEqual(user.full_name, 'Adam Anderson')

    def test_to_dict(self):
        """It serlializes as a dict representation"""
        attrs = {'id': 1, 'name': 'Eggs and Spam'}
        breakfast = BreakfastFactory.build(**attrs)
        self.assertDictEqual(breakfast.to_dict(), attrs)


class IngredientTestCase(OrmTestCase, BaseTestCase):

    def test_to_dict(self):
        """It serlializes as a dict representation"""
        attrs = {'id': 1, 'name': 'Spam'}
        ingredient = IngredientFactory.build(**attrs)
        self.assertDictEqual(ingredient.to_dict(), attrs)
