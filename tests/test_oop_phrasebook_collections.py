import mock

from . import BaseTestCase
from .mixins import PhrasebookFixturedTestCase
from eggsnspam.oop_phrasebook.models import (BreakfastModel, IngredientModel,
                                             UserModel, UserPreferenceModel)
from eggsnspam.oop_phrasebook.collections import (BreakfastCollection, IngredientCollection,
                                                  UserCollection, UserPreferenceCollection)


class BreakfastCollectionTestCase(PhrasebookFixturedTestCase, BaseTestCase):

    def test_create_model(self):
        """It creates a model instance"""
        breakfast_collection = BreakfastCollection()
        breakfast = breakfast_collection.create_model(data={'id': 1, 'name': 'Karma'})
        self.assertIsInstance(breakfast, BreakfastModel)
        self.assertEqual(breakfast.id, 1)
        self.assertEqual(breakfast.name, 'Karma')

    @mock.patch('eggsnspam.oop_phrasebook.daos.SqlBaseDao.fetchall')
    def test_load_all(self, m_fetchall):
        """It gets all the breakfasts from the database"""
        m_fetchall.return_value = [{'id': 1, 'name': 'Argyle'},
                                   {'id': 2, 'name': 'Benedict'}]
        breakfast_collection = BreakfastCollection()
        self.assertTrue(breakfast_collection.load_all())
        self.assertTrue(m_fetchall.called)
        self.assertEqual(len(breakfast_collection.models), 2)
        self.assertEqual(breakfast_collection.models[0].id, 1)
        self.assertEqual(breakfast_collection.models[1].id, 2)


class IngredientCollectionTestCase(PhrasebookFixturedTestCase, BaseTestCase):

    def test_create_model(self):
        """It creates a model instance"""
        ingredient_collection = IngredientCollection()
        ingredient = ingredient_collection.create_model(data={'id': 1, 'name': 'Karma'})
        self.assertIsInstance(ingredient, IngredientModel)
        self.assertEqual(ingredient.id, 1)
        self.assertEqual(ingredient.name, 'Karma')

    @mock.patch('eggsnspam.oop_phrasebook.daos.SqlBaseDao.fetchall')
    def test_load_all(self, m_fetchall):
        """It gets all the ingredients from the database"""
        m_fetchall.return_value = [{'id': 1, 'name': 'Argyle'},
                                   {'id': 2, 'name': 'Benedict'}]
        ingredient_collection = IngredientCollection()
        self.assertTrue(ingredient_collection.load_all())
        self.assertTrue(m_fetchall.called)
        self.assertEqual(len(ingredient_collection.models), 2)
        self.assertEqual(ingredient_collection.models[0].id, 1)
        self.assertEqual(ingredient_collection.models[1].id, 2)


class UserCollectionTestCase(PhrasebookFixturedTestCase, BaseTestCase):

    def test_create_model(self):
        """It creates a model instance"""
        user_collection = UserCollection()
        user = user_collection.create_model(data={'id': 1, 'first_name': 'Karma', 'last_name': 'Kabana'})
        self.assertIsInstance(user, UserModel)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.first_name, 'Karma')
        self.assertEqual(user.last_name, 'Kabana')

    @mock.patch('eggsnspam.oop_phrasebook.daos.SqlBaseDao.fetchall')
    def test_load_all(self, m_fetchall):
        """It gets all the Users from the database"""
        m_fetchall.return_value = [{'id': 1, 'first_name': 'Argyle', 'last_name': 'Armani'},
                                   {'id': 2, 'first_name': 'Benedict', 'last_name': 'Bernardo'}]
        user_collection = UserCollection()
        self.assertTrue(user_collection.load_all())
        self.assertTrue(m_fetchall.called)
        self.assertEqual(len(user_collection.models), 2)
        self.assertEqual(user_collection.models[0].id, 1)
        self.assertEqual(user_collection.models[1].id, 2)


class UserPreferenceCollectionTestCase(PhrasebookFixturedTestCase, BaseTestCase):

    def test_create_model(self):
        """It creates a model instance"""
        user_pref_collection = UserPreferenceCollection()
        user_pref = user_pref_collection.create_model(
            data={'id': 1, 'user_id': 123, 'ingredient_id': 456, 'coefficient': 0.8})
        self.assertIsInstance(user_pref, UserPreferenceModel)
        self.assertEqual(user_pref.id, 1)
        self.assertEqual(user_pref.user_id, 123)
        self.assertEqual(user_pref.ingredient_id, 456)
        self.assertEqual(user_pref.coefficient, 0.8)

    @mock.patch('eggsnspam.oop_phrasebook.daos.SqlBaseDao.fetchall')
    def test_load_all_for_user(self, m_fetchall):
        """It gets all the Users from the database"""
        m_fetchall.return_value = [{'coefficient': 0.8, 'ingredient_id': 1, 'user_id': 1, 'id': 1},
                                   {'coefficient': 0.8, 'ingredient_id': 2, 'user_id': 1, 'id': 2}]
        user_pref_collection = UserPreferenceCollection()
        self.assertTrue(user_pref_collection.load_all_for_user(1))
        self.assertTrue(m_fetchall.called)
        self.assertEqual(len(user_pref_collection.models), 2)
        self.assertEqual(user_pref_collection.models[0].id, 1)
        self.assertEqual(user_pref_collection.models[1].id, 2)
