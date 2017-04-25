from . import BaseTestCase
from eggsnspam.oop_phrasebook.daos import (BreakfastDao, IngredientDao, UserDao,
                                           UserPreferenceDao, BreakfastIngredientDao)
from .mixins import PhrasebookFixturedTestCase


class BreakfastDaoTestCase(PhrasebookFixturedTestCase, BaseTestCase):

    def setUp(self):
        super(BreakfastDaoTestCase, self).setUp()
        self.dao = BreakfastDao()

    def test_get_by_id(self):
        """It gets a record by matching an ID"""
        result = self.dao.get_by_id(1)
        self.assertDictEqual(result, {'id': 1, 'name': 'Eggs and Spam'})
        result = self.dao.get_by_id(-1)
        self.assertEqual(result, None)

    def test_list_all(self):
        """It gets all records from the database"""
        result = self.dao.list_all()
        self.assertEqual(len(result), 3)
        self.assertDictEqual(result[0], {'id': 1, 'name': 'Eggs and Spam'})


class IngredientDaoTestCase(PhrasebookFixturedTestCase, BaseTestCase):

    def setUp(self):
        super(IngredientDaoTestCase, self).setUp()
        self.dao = IngredientDao()

    def test_get_by_id(self):
        """It gets a record by matching an ID"""
        result = self.dao.get_by_id(1)
        self.assertDictEqual(result, {'id': 1, 'name': 'Eggs'})
        result = self.dao.get_by_id(-1)
        self.assertEqual(result, None)

    def test_list_all(self):
        """It gets all records from the database"""
        result = self.dao.list_all()
        self.assertEqual(len(result), 3)
        self.assertDictEqual(result[0], {'id': 1, 'name': 'Eggs'})


class UserDaoTestCase(PhrasebookFixturedTestCase, BaseTestCase):

    def setUp(self):
        super(UserDaoTestCase, self).setUp()
        self.dao = UserDao()

    def test_get_by_id(self):
        """It gets a record by matching an ID"""
        result = self.dao.get_by_id(1)
        self.assertDictEqual(result, {'id': 1, 'first_name': 'Adam', 'last_name': 'Anderson'})
        result = self.dao.get_by_id(-1)
        self.assertEqual(result, None)

    def test_create(self):
        """It creates a new record"""
        result = self.dao.create(first_name='Darma', last_name='Dallas')
        self.assertTrue(isinstance(result, int))

    def test_update(self):
        """It updates records in the database"""
        result = self.dao.update(1, first_name='Mada', last_name='Nosredna')
        self.assertTrue(result)

        # expect method to return False if no records matched the ID
        result = self.dao.update(-1, first_name='Mada', last_name='Nosredna')
        self.assertFalse(result)

    def test_delete(self):
        """It deletes records from the database"""
        result = self.dao.delete(1)
        self.assertTrue(result)

        # expect the result to be False if no records matched the ID
        result = self.dao.delete(1)
        self.assertFalse(result)

    def test_list_all(self):
        """It gets all records from the database"""
        result = self.dao.list_all()
        self.assertEqual(len(result), 4)
        self.assertDictEqual(result[0], {'id': 1, 'first_name': 'Adam', 'last_name': 'Anderson'})

    def test_get_by_id_join_preferences(self):
        """It gets a user and all of its ingredient preferences"""

        # expect a user who does not exist to return None
        result = self.dao.get_by_id_join_preferences(0)
        self.assertIsNone(result, 0)

        # expect a user with no pereferences to have an empty array
        result = self.dao.get_by_id_join_preferences(4)
        self.assertEqual(result['id'], 4)
        self.assertEqual(result['preferences'], {})

        # expect a user with preferences to have an array of preferences
        result = self.dao.get_by_id_join_preferences(1)
        self.assertEqual(result['id'], 1)
        self.assertEqual(len(list(result['preferences'].keys())), 3)
        self.assertEqual(result['preferences'][1], 0.8)
        self.assertEqual(result['preferences'][2], 0.4)
        self.assertEqual(result['preferences'][3], 0.6)


class UserPreferenceDaoTestCase(PhrasebookFixturedTestCase, BaseTestCase):

    def setUp(self):
        super(UserPreferenceDaoTestCase, self).setUp()
        self.dao = UserPreferenceDao()

    def test_create(self):
        """It creates a new record"""
        result = self.dao.create(user_id=4, ingredient_id=1, coefficient=1)
        self.assertTrue(isinstance(result, int))

    def test_get_by_id(self):
        """It gets a record by matching an ID"""
        result = self.dao.create(user_id=4, ingredient_id=1, coefficient=0.8)
        result = self.dao.get_by_id(result)
        self.assertDictIsSuperset(result, {'coefficient': 0.8, 'user_id': 4, 'ingredient_id': 1})
        result = self.dao.get_by_id(-1)
        self.assertEqual(result, None)

    def test_get_by_user_ingredient(self):
        """It gets a record by matching an ID"""
        result = self.dao.get_by_user_ingredient(user_id=1, ingredient_id=1)
        self.assertDictIsSuperset(result, {'coefficient': 0.8, 'ingredient_id': 1, 'user_id': 1})
        result = self.dao.get_by_user_ingredient(user_id=-1, ingredient_id=1)
        self.assertEqual(result, None)

    def test_list_all_for_user(self):
        """It gets all records from the database"""
        result = self.dao.list_all_for_user(1)
        self.assertEqual(len(result), 3)
        self.assertDictIsSuperset(result[0], {'coefficient': 0.8, 'ingredient_id': 1, 'user_id': 1})

    def test_update(self):
        """It updates records in the database"""
        id_to_update = self.dao.create(user_id=4, ingredient_id=1, coefficient=0.8)
        result = self.dao.update(id_to_update, user_id=1, ingredient_id=1, coefficient=0.1)
        self.assertTrue(result)

        # expect method to return False if no records matched the ID
        result = self.dao.update(-1, user_id=1, ingredient_id=1, coefficient=0.1)
        self.assertFalse(result)

    def test_delete(self):
        """It deletes records from the database"""
        id_to_delete = self.dao.create(user_id=4, ingredient_id=1, coefficient=0.8)
        result = self.dao.delete(id_to_delete)
        self.assertTrue(result)

        # expect the result to be False if no records matched the ID
        result = self.dao.delete(id_to_delete)
        self.assertFalse(result)


class BreakfastIngredientTestCase(PhrasebookFixturedTestCase, BaseTestCase):

    def setUp(self):
        super(BreakfastIngredientTestCase, self).setUp()
        self.dao = BreakfastIngredientDao()

    def test_list_all(self):
        """It gets all records from the database"""
        result = self.dao.list_all()
        self.assertEqual(len(result), 9)
        self.assertDictEqual(result[0], {'breakfast_id': 1, 'coefficient': 0.8, 'ingredient_id': 1})
