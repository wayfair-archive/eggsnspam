import mock

from . import BaseTestCase
from .mixins import PhrasebookFixturedTestCase
from eggsnspam.oop_phrasebook.models import BreakfastModel, IngredientModel, UserModel, UserPreferenceModel


class BreakfastModelTestCase(PhrasebookFixturedTestCase, BaseTestCase):

    def test_load_by_id(self):
        """It loads a model instance by its ID"""
        mock_dao = mock.MagicMock()
        mock_dao.get_by_id.return_value = {'id': 1, 'name': 'Eggs and Spam'}

        breakfast = BreakfastModel(mock_dao)
        breakfast.load_by_id(1)
        self.assertEqual(breakfast.id, 1)
        self.assertEqual(breakfast.name, 'Eggs and Spam')

        # expect value error to be raised if no record is found
        mock_dao.get_by_id.return_value = None
        breakfast_no_result = BreakfastModel(dao=mock_dao)
        with self.assertRaises(ValueError):
            breakfast_no_result.load_by_id(-1)

    def test_populate(self):
        """It populates model properties from a map of values"""
        breakfast = BreakfastModel()
        breakfast.populate({'name': 'Eggs'})
        self.assertEqual(breakfast.name, 'Eggs')

    def test_to_dict(self):
        """It serlializes as a dict representation"""

        breakfast = BreakfastModel()
        breakfast.id = 1
        breakfast.name = 'Eggs and Spam'

        self.assertDictEqual(breakfast.to_dict(), {'id': 1, 'name': 'Eggs and Spam'})


class IngredientModelTestCase(PhrasebookFixturedTestCase, BaseTestCase):

    def test_load_by_id(self):
        """It loads a model instance by its ID"""
        mock_dao = mock.MagicMock()
        mock_dao.get_by_id.return_value = {'id': 1, 'name': 'Eggs'}

        ingredient = IngredientModel(mock_dao)
        ingredient.load_by_id(1)
        self.assertEqual(ingredient.id, 1)
        self.assertEqual(ingredient.name, 'Eggs')

        # expect value error to be raised if no record is found
        mock_dao.get_by_id.return_value = None
        ingredient_no_result = IngredientModel(dao=mock_dao)
        with self.assertRaises(ValueError):
            ingredient_no_result.load_by_id(-1)

    def test_populate(self):
        """It populates model properties from a map of values"""
        ingredient = IngredientModel()
        ingredient.populate({'name': 'Eggs'})
        self.assertEqual(ingredient.name, 'Eggs')

    def test_to_dict(self):
        """It serlializes as a dict representation"""

        ingredient = IngredientModel()
        ingredient.id = 1
        ingredient.name = 'Eggs'

        self.assertDictEqual(ingredient.to_dict(), {'id': 1, 'name': 'Eggs'})


class UserModelTestCase(PhrasebookFixturedTestCase, BaseTestCase):

    def test_full_name(self):
        """It returns a person's full name"""
        user = UserModel()
        user.first_name = 'Adam'
        user.last_name = 'Anderson'
        self.assertEqual(user.full_name, 'Adam Anderson')

    def test_load_by_id(self):
        """It loads a model instance by its ID"""
        mock_dao = mock.MagicMock()
        mock_dao.get_by_id.return_value = {'id': 1, 'first_name': 'Adam', 'last_name': 'Anderson'}

        user = UserModel(mock_dao)
        user.load_by_id(1)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.first_name, 'Adam')
        self.assertEqual(user.last_name, 'Anderson')

        # expect value error to be raised if no record is found
        mock_dao.get_by_id.return_value = None
        user_no_result = UserModel(dao=mock_dao)
        with self.assertRaises(ValueError):
            user_no_result.load_by_id(-1)

    def test_load_by_id_with_preferences(self):
        """It loads a model instance by its ID and joins ingredient preferences"""
        mock_dao = mock.MagicMock()
        mock_dao.get_by_id.return_value = {'id': 1, 'first_name': 'Adam', 'last_name': 'Anderson', 'preferences': []}

        user_no_prefs = UserModel(mock_dao)
        user_no_prefs.load_by_id(1)
        self.assertEqual(user_no_prefs.preferences, [])

        mock_preferences = [
            {'ingredient_id': 1, 'coefficient': 0.5},
            {'ingredient_id': 2, 'coefficient': 0.1},
        ]
        mock_dao.get_by_id.return_value = {
            'id': 1,
            'first_name': 'Adam',
            'last_name': 'Anderson',
            'preferences': mock_preferences
        }

        # expect value error to be raised if no record is found
        user_with_prefs = UserModel(dao=mock_dao)
        user_with_prefs.load_by_id(1)
        self.assertEqual(user_with_prefs.preferences, mock_preferences)

    def test_populate(self):
        """It populates model properties from a map of values"""
        user = UserModel()
        user.populate({'first_name': 'Adam', 'last_name': 'Anderson'})
        self.assertEqual(user.full_name, 'Adam Anderson')

    def test_validate(self):
        """It validates the models properties"""
        user = UserModel()

        # Expect user to be invalid because there is no last name
        user.first_name = "Tom"
        self.assertFalse(user.validate())

        # Expect a user with first name and last name to be valid
        user.last_name = "Tabarau"
        self.assertTrue(user.validate())

        # Expect a unicode name to be valid
        user.first_name = "Tom"
        user.last_name = "Tabarau"
        self.assertTrue(user.validate())

    @mock.patch.object(UserModel, "validate", return_value=True)
    def test_save(self, m_validate):
        """It saves a model instance"""
        mock_dao = mock.MagicMock()

        # Expect a new model to be created if no ID is set
        mock_dao.create.return_value = 101
        user = UserModel(mock_dao)
        user.first_name = 'Carlton'
        user.last_name = 'Camaro'
        user.save()
        self.assertTrue(mock_dao.create.called)
        self.assertEqual(user.id, 101)
        self.assertDictEqual(mock_dao.create.call_args[1],
                             {'first_name': 'Carlton', 'last_name': 'Camaro'})

        # Expect a model instance to be updated if an ID is set
        user.first_name = 'Darl'
        user.last_name = 'Dominic'
        user.save()
        self.assertTrue(mock_dao.update.called)
        self.assertDictEqual(mock_dao.update.call_args[1],
                             {'first_name': 'Darl', 'last_name': 'Dominic'})

        # Expect a ValueError to be raised if validate returns False
        m_validate.return_value = False
        user.last_name = None
        with self.assertRaises(ValueError):
            user.save()

    def test_delete(self):
        """It deletes a model instance from the database"""
        mock_dao = mock.MagicMock()
        mock_dao.delete.return_value = True

        user = UserModel(mock_dao)
        user.id = 1

        # expect a user to be deleted from the dao
        self.assertTrue(user.delete())
        self.assertTrue(mock_dao.delete.called)
        self.assertEqual(mock_dao.delete.call_args[0][0], 1)
        self.assertIsNone(user.id)

        # expect trying to delete a user with no
        mock_dao.delete.reset_mock()
        self.assertFalse(user.delete())
        self.assertFalse(mock_dao.delete.called)

    def test_to_dict(self):
        """It serlializes as a dict representation"""

        user = UserModel()
        user.id = 1
        user.first_name = 'Karma'
        user.last_name = 'Kabana'

        self.assertDictEqual(user.to_dict(), {'id': 1, 'first_name': 'Karma', 'last_name': 'Kabana'})

    def test_get_recommendations(self):
        """It gets recommended breakfasts"""
        user = UserModel()
        user.id = 1
        user.first_name = 'Karma'
        user.last_name = 'Kabana'

        mock_dao = mock.MagicMock()
        mock_dao.list_all.return_value = [
            {'breakfast_id': 1, 'ingredient_id': 1, 'coefficient': 0.8},
            {'breakfast_id': 1, 'ingredient_id': 2, 'coefficient': 0.8},
            {'breakfast_id': 1, 'ingredient_id': 3, 'coefficient': 0.2},
            {'breakfast_id': 2, 'ingredient_id': 1, 'coefficient': 0.0},
            {'breakfast_id': 2, 'ingredient_id': 2, 'coefficient': 0.2},
            {'breakfast_id': 2, 'ingredient_id': 3, 'coefficient': 0.9},
            {'breakfast_id': 3, 'ingredient_id': 1, 'coefficient': 0.9},
            {'breakfast_id': 3, 'ingredient_id': 2, 'coefficient': 0.5},
            {'breakfast_id': 3, 'ingredient_id': 3, 'coefficient': 0.1}
        ]

        # Expect a value error if we have not loaded recommendations
        with self.assertRaises(ValueError):
            user.get_recommendations()

        # Expect an empty list if a user has no preferences
        user.preferences = {}
        self.assertEqual(user.get_recommendations(), [])

        # Expect an empty list if a user has no preferences
        user.preferences = {
            2: 0.4,
            3: 0.5
        }
        recommendations = user.get_recommendations()
        self.assertEqual(len(recommendations), 3)
        self.assertEqual(recommendations[0]['breakfast_id'], 2)
        self.assertEqual(recommendations[1]['breakfast_id'], 1)
        self.assertEqual(recommendations[2]['breakfast_id'], 3)
        self.assertEqual(recommendations[2]['score'], 0.25)


class UserPreferenceModelTestCase(PhrasebookFixturedTestCase, BaseTestCase):

    def test_load_by_id(self):
        """It loads a model instance by its ID"""
        mock_dao = mock.MagicMock()
        mock_dao.get_by_id.return_value = {'id': 1, 'user_id': 1, 'ingredient_id': 4, 'coefficient': 0.8}

        pref = UserPreferenceModel(mock_dao)
        pref.load_by_id(1)
        self.assertEqual(pref.id, 1)
        self.assertEqual(pref.user_id, 1)
        self.assertEqual(pref.ingredient_id, 4)
        self.assertEqual(pref.coefficient, 0.8)

        # expect value error to be raised if no record is found
        mock_dao.get_by_id.return_value = None
        user_no_result = UserPreferenceModel(dao=mock_dao)
        with self.assertRaises(ValueError):
            user_no_result.load_by_id(-1)

    def test_load_by_user_ingredient(self):
        """It loads a model instance by its ID"""
        mock_dao = mock.MagicMock()
        mock_dao.get_by_user_ingredient.return_value = {'id': 1, 'user_id': 1, 'ingredient_id': 4, 'coefficient': 0.8}

        pref = UserPreferenceModel(mock_dao)
        pref.load_by_user_ingredient(1, 1)
        self.assertEqual(pref.id, 1)
        self.assertEqual(pref.user_id, 1)
        self.assertEqual(pref.ingredient_id, 4)
        self.assertEqual(pref.coefficient, 0.8)

        # expect value error to be raised if no record is found
        mock_dao.get_by_user_ingredient.return_value = None
        user_no_result = UserPreferenceModel(dao=mock_dao)
        with self.assertRaises(ValueError):
            user_no_result.load_by_user_ingredient(-1, 1)

    def test_populate(self):
        """It populates model properties from a map of values"""
        pref = UserPreferenceModel()
        pref.populate({'id': 1, 'user_id': 2, 'ingredient_id': 3, 'coefficient': 0.5})
        self.assertEqual(pref.id, 1)
        self.assertEqual(pref.user_id, 2)
        self.assertEqual(pref.ingredient_id, 3)
        self.assertEqual(pref.coefficient, 0.5)

    def test_validate(self):
        """It validates the models properties"""
        pref = UserPreferenceModel()

        # Expect user to be invalid because there is no last name
        pref.user_id = 1
        self.assertFalse(pref.validate())

        # Expect a user with first name and last name to be valid
        pref.ingredient_id = 1
        pref.coefficient = 0.5
        self.assertTrue(pref.validate())

        # Expect a string id to be invalid
        pref.user_id = "1"
        self.assertFalse(pref.validate())
        pref.user_id = 1

        # Expect a coefficient value > 1 to be invalid
        pref.coefficient = 1.1
        self.assertFalse(pref.validate())
        pref.coefficient = 0.5

    @mock.patch.object(UserPreferenceModel, "validate", return_value=True)
    def test_save(self, m_validate):
        """It saves a model instance"""
        mock_dao = mock.MagicMock()

        # Expect a new model to be created if no ID is set
        mock_dao.create.return_value = 101
        pref = UserPreferenceModel(mock_dao)
        pref.user_id = 1
        pref.ingredient_id = 2
        pref.coefficient = 0.5
        pref.save()
        self.assertTrue(mock_dao.create.called)
        self.assertEqual(pref.id, 101)
        self.assertDictEqual(mock_dao.create.call_args[1],
                             {'user_id': 1, 'ingredient_id': 2, 'coefficient': 0.5})

        # Expect a model instance to be updated if an ID is set
        pref.coefficient = 0.9
        pref.save()
        self.assertTrue(mock_dao.update.called)
        self.assertDictEqual(mock_dao.update.call_args[1],
                             {'id': 101, 'user_id': 1, 'ingredient_id': 2, 'coefficient': 0.9})

        # Expect a ValueError to be raised if validate returns False
        m_validate.return_value = False
        pref.last_name = None
        with self.assertRaises(ValueError):
            pref.save()

    def test_delete(self):
        """It deletes a model instance from the database"""
        mock_dao = mock.MagicMock()
        mock_dao.delete.return_value = True

        pref = UserPreferenceModel(mock_dao)
        pref.id = 1

        # expect a model instance to be deleted from the dao
        self.assertTrue(pref.delete())
        self.assertTrue(mock_dao.delete.called)
        self.assertEqual(mock_dao.delete.call_args[0][0], 1)
        self.assertIsNone(pref.id)

        # expect trying to delete a pref with no
        mock_dao.delete.reset_mock()
        self.assertFalse(pref.delete())
        self.assertFalse(mock_dao.delete.called)

    def test_to_dict(self):
        """It serlializes as a dict representation"""

        pref = UserPreferenceModel()
        pref.id = 101
        pref.user_id = 1
        pref.ingredient_id = 2
        pref.coefficient = 0.9

        self.assertDictEqual(pref.to_dict(), {'id': 101, 'user_id': 1, 'ingredient_id': 2, 'coefficient': 0.9})
