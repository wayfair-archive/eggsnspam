import json
import mock

from . import BaseTestCase
from .mixins import HealthViewTestCaseMixin


class HealthViewTestCase(HealthViewTestCaseMixin, BaseTestCase):
    """Testcase for healthcheck endpoint"""

    base_url_path = '/oop_phrasebook'


class BreakfastTestCase(BaseTestCase):

    @mock.patch('eggsnspam.oop_phrasebook.daos.BreakfastDao.list_all')
    def test_list_breakfasts(self, m_list_all):
        """It lists all the breakfasts in the database"""

        m_list_all.return_value = []

        # expect no breakfasts to return an empty json object
        response = self.client.get("/oop_phrasebook/breakfast/",
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json
        self.assertIn("breakfasts", response_data)
        self.assertTrue(m_list_all.called)
        self.assertEqual(len(response_data["breakfasts"]), 0)

        # mock 3 breakfasts
        m_results = [
            {'id': 1, 'name': 'Eggs'},
            {'id': 2, 'name': 'Fruit Cup'},
            {'id': 3, 'name': 'Pancakes'},
        ]
        m_list_all.return_value = m_results
        breakfast_ids = [x['id'] for x in m_results]

        # exepect 3 breakfast objects to be returned
        response = self.client.get("/oop_phrasebook/breakfast/",
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json
        self.assertEqual(len(response_data['breakfasts']), len(m_results))
        for breakfast in response_data['breakfasts']:
            self.assertIn(breakfast['id'], breakfast_ids)

    @mock.patch('eggsnspam.oop_phrasebook.daos.BreakfastDao.get_by_id')
    def test_get_breakfast(self, m_get_by_id):
        """It lists all the breakfasts in the database"""

        # expect to get a 404 response if no breakfast found for ID
        m_get_by_id.return_value = None
        response = self.client.get("/oop_phrasebook/breakfast/-1",
                                   content_type='application/json')
        self.assertEqual(response.status_code, 404)

        # expect to get a json object representation of a breakfast to be returned
        mocked_breakfast_data = {'id': 1, 'name': 'Eggs'}
        m_get_by_id.return_value = mocked_breakfast_data
        response = self.client.get("/oop_phrasebook/breakfast/{}".format(mocked_breakfast_data['id']),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json
        self.assertEqual(response_data['id'], mocked_breakfast_data['id'])
        self.assertEqual(response_data['name'], mocked_breakfast_data['name'])


class IngredientTestCase(BaseTestCase):

    @mock.patch('eggsnspam.oop_phrasebook.daos.IngredientDao.list_all')
    def test_list_ingredients(self, m_list_all):
        """It lists all the ingredients in the database"""

        m_list_all.return_value = []

        # expect no ingredients to return an empty json object
        response = self.client.get("/oop_phrasebook/ingredient/",
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json
        self.assertIn("ingredients", response_data)
        self.assertTrue(m_list_all.called)
        self.assertEqual(len(response_data["ingredients"]), 0)

        # mock 3 ingredients
        m_results = [
            {'id': 1, 'name': 'Eggs'},
            {'id': 2, 'name': 'Fruit Cup'},
            {'id': 3, 'name': 'Pancakes'},
        ]
        m_list_all.return_value = m_results
        ingredient_ids = [x['id'] for x in m_results]

        # exepect 3 ingredient objects to be returned
        response = self.client.get("/oop_phrasebook/ingredient/",
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json
        self.assertEqual(len(response_data['ingredients']), len(m_results))
        for ingredient in response_data['ingredients']:
            self.assertIn(ingredient['id'], ingredient_ids)

    @mock.patch('eggsnspam.oop_phrasebook.daos.IngredientDao.get_by_id')
    def test_get_ingredient(self, m_get_by_id):
        """It lists all the ingredients in the database"""

        # expect to get a 404 response if no ingredient found for ID
        m_get_by_id.return_value = None
        response = self.client.get("/oop_phrasebook/ingredient/-1",
                                   content_type='application/json')
        self.assertEqual(response.status_code, 404)

        # expect to get a json object representation of a ingredient to be returned
        mocked_ingredient_data = {'id': 1, 'name': 'Eggs'}
        m_get_by_id.return_value = mocked_ingredient_data
        response = self.client.get("/oop_phrasebook/ingredient/{}".format(mocked_ingredient_data['id']),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json
        self.assertEqual(response_data['id'], mocked_ingredient_data['id'])
        self.assertEqual(response_data['name'], mocked_ingredient_data['name'])


class UserTestCase(BaseTestCase):

    @mock.patch('eggsnspam.oop_phrasebook.daos.UserDao.list_all')
    def test_list_users(self, m_list_all):
        """It lists all the users in the database"""

        m_list_all.return_value = []

        # expect no users to return an empty json object
        response = self.client.get("/oop_phrasebook/user/",
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json
        self.assertIn("users", response_data)
        self.assertTrue(m_list_all.called)
        self.assertEqual(len(response_data["users"]), 0)

        # mock 3 users
        m_results = [
            {'id': 1, 'first_name': 'Adam', 'last_name': 'Anderson'},
            {'id': 2, 'first_name': 'Betty', 'last_name': 'Blevins'},
            {'id': 3, 'first_name': 'Carl', 'last_name': 'Cadigan'},
        ]
        m_list_all.return_value = m_results
        user_ids = [x['id'] for x in m_results]

        # exepect 3 user objects to be returned
        response = self.client.get("/oop_phrasebook/user/",
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json
        self.assertEqual(len(response_data['users']), len(m_results))
        for user in response_data['users']:
            self.assertIn(user['id'], user_ids)

    @mock.patch('eggsnspam.oop_phrasebook.daos.UserDao.create')
    def test_create_user(self, m_create):
        """It creates a user record in the database"""
        m_create.return_value = 1

        # expect a 400 error if invalid data is provided
        response = self.client.post("/oop_phrasebook/user/",
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

        request_data = {
            "first_name": "Harrison",
            "last_name": "Ford"
        }

        # expect a 201 response if we created an object
        response = self.client.post("/oop_phrasebook/user/",
                                    data=json.dumps(request_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)

        # expect the json reprisentation of the user to be returned
        response_data = response.json
        self.assertEqual(response_data['id'], 1)
        self.assertEqual(response_data['first_name'], request_data['first_name'])
        self.assertEqual(response_data['last_name'], request_data['last_name'])

    @mock.patch('eggsnspam.oop_phrasebook.daos.UserDao.get_by_id')
    def test_get_user(self, m_get_by_id):
        """It lists all the users in the database"""

        # expect to get a 404 response if no user found for ID
        m_get_by_id.return_value = None
        response = self.client.get("/oop_phrasebook/user/-1",
                                   content_type='application/json')
        self.assertEqual(response.status_code, 404)

        # expect to get a json object representation of a user to be returned
        mocked_user_data = {'id': 1, 'first_name': 'Adam', 'last_name': 'Anderson'}
        m_get_by_id.return_value = mocked_user_data
        response = self.client.get("/oop_phrasebook/user/{}".format(mocked_user_data['id']),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json
        self.assertEqual(response_data['id'], mocked_user_data['id'])
        self.assertEqual(response_data['first_name'], mocked_user_data['first_name'])
        self.assertEqual(response_data['last_name'], mocked_user_data['last_name'])

    @mock.patch('eggsnspam.oop_phrasebook.daos.BreakfastIngredientDao.list_all')
    @mock.patch('eggsnspam.oop_phrasebook.daos.UserDao.get_by_id_join_preferences')
    def test_breakfast_recommendations(self, m_get_by_id_join_preferences, m_list_all):
        """It returns the recommended breakfasts for a user"""

        # Expect a 404 resposne code if the user does not exist
        m_list_all.return_value = [
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

        m_get_by_id_join_preferences.return_value = None
        response = self.client.get("/oop_phrasebook/user/0/breakfast_recommendations",
                                   content_type='application/json')
        self.assertEqual(response.status_code, 404)

        # Expect recommendations to be returned for a user with preferences
        m_get_by_id_join_preferences.return_value = {
            'id': 1,
            'first_name': 'Adam',
            'last_name': 'Anderson',
            'preferences': {
                0: 0.8,
                1: 0.4,
                2: 0.6,
            }

        }
        response = self.client.get("/oop_phrasebook/user/1/breakfast_recommendations",
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json
        self.assertIn('breakfast_recs', response_data)
        self.assertEqual(len(response_data['breakfast_recs']), 3)
        self.assertTrue('breakfast_id' in response_data['breakfast_recs'][0])
        self.assertTrue('score' in response_data['breakfast_recs'][0])

    @mock.patch('eggsnspam.oop_phrasebook.daos.UserDao.get_by_id')
    @mock.patch('eggsnspam.oop_phrasebook.daos.UserDao.update')
    def test_update_user(self, m_update, m_get_by_id):
        """It updates a user in the database"""
        request_data = {
            "first_name": "Beta",
            "last_name": "Baboon"
        }

        # expect to get a 404 response if no user found for ID
        m_get_by_id.return_value = None
        response = self.client.put("/oop_phrasebook/user/-1",
                                   content_type='application/json')
        self.assertEqual(response.status_code, 404)

        # expect a json representation of the updated user to be returned
        m_get_by_id.return_value = {'id': 1, 'first_name': 'Adam', 'last_name': 'Anderson'}
        m_update.return_value = 1
        response = self.client.put("/oop_phrasebook/user/1",
                                   content_type='application/json',
                                   data=json.dumps(request_data))
        self.assertEqual(response.status_code, 200)
        response_data = response.json
        self.assertEqual(response_data['first_name'], request_data['first_name'])
        self.assertEqual(response_data['last_name'], request_data['last_name'])
        self.assertEqual(m_update.call_args[1]['first_name'], request_data['first_name'])
        self.assertEqual(m_update.call_args[1]['last_name'], request_data['last_name'])

    @mock.patch('eggsnspam.oop_phrasebook.daos.UserDao.get_by_id')
    @mock.patch('eggsnspam.oop_phrasebook.daos.UserDao.delete')
    def test_delete_user(self, m_delete, m_get_by_id):
        """It creates a user record in the database"""

        # expect a 404 error if no record matches the ID
        m_get_by_id.return_value = None
        response = self.client.delete("/oop_phrasebook/user/-1")
        self.assertEqual(response.status_code, 404)

        # expect an object to be deleted if it is found
        m_get_by_id.return_value = {'id': 1, 'first_name': 'Adam', 'last_name': 'Anderson'}
        m_delete.return_value = True
        response = self.client.delete("/oop_phrasebook/user/1")
        self.assertEqual(response.status_code, 204)

        # expect an failed database call to return an error
        m_get_by_id.return_value = {'id': 1, 'first_name': 'Adam', 'last_name': 'Anderson'}
        m_delete.return_value = False
        response = self.client.delete("/oop_phrasebook/user/1")
        self.assertEqual(response.status_code, 500)


class UserPreferencesTestCase(BaseTestCase):

    list_url_template = "/oop_phrasebook/user/{user_id}/preference/"
    detail_url_template = "/oop_phrasebook/user/{user_id}/preference/{ingredient_id}"

    def setUp(self):
        super(UserPreferencesTestCase, self).setUp()

        # create a user for each test
        self.user_id = 1
        self.list_url = self.list_url_template.format(user_id=self.user_id)

    @mock.patch('eggsnspam.oop_phrasebook.daos.UserDao.get_by_id')
    @mock.patch('eggsnspam.oop_phrasebook.daos.UserPreferenceDao.list_all_for_user')
    def test_list_user_preferences(self, m_list_all_for_user, m_get_by_id):
        """It lists all the user preferences in the database"""

        m_list_all_for_user.return_value = []

        # expect 404 if user does not exist
        m_get_by_id.return_value = None
        response = self.client.get(self.list_url_template.format(user_id=0), content_type='application/json')
        self.assertEqual(response.status_code, 404)

        # expect no user preferences to return an empty json object
        m_get_by_id.return_value = {'id': 1, 'first_name': 'Adam', 'last_name': 'Anderson'}
        response = self.client.get(self.list_url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json
        self.assertIn("user_preferences", response_data)
        self.assertEqual(len(response_data["user_preferences"]), 0)

        # create 3 user preferences
        prefs = [
            {'id': 1, 'user_id': 1, 'ingredient_id': 4, 'coefficient': 0.8},
            {'id': 2, 'user_id': 1, 'ingredient_id': 5, 'coefficient': 0.7},
            {'id': 3, 'user_id': 1, 'ingredient_id': 6, 'coefficient': 0.9}
        ]
        m_list_all_for_user.return_value = prefs

        # exepect 3 objects to be returned
        response = self.client.get(self.list_url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json
        self.assertIn("user_preferences", response_data)
        self.assertEqual(len(response_data["user_preferences"]), 3)

    @mock.patch('eggsnspam.oop_phrasebook.daos.UserPreferenceDao.create')
    @mock.patch('eggsnspam.oop_phrasebook.daos.UserDao.get_by_id')
    def test_create_user_preference(self, m_get_by_id, m_create):
        """It creates a user preference record in the database"""

        m_create.return_value = 1

        # expect 404 if user does not exist
        m_get_by_id.return_value = None
        response = self.client.post(self.list_url_template.format(user_id=0), content_type='application/json')
        self.assertEqual(response.status_code, 404)

        # expect a 400 error if invalid data is provided
        m_get_by_id.return_value = {'id': 1, 'first_name': 'Adam', 'last_name': 'Anderson'}
        response = self.client.post(self.list_url, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # new object payload
        request_data = {'ingredient_id': 4, 'coefficient': 0.8}

        # expect a 201 response if we created an object
        response = self.client.post(self.list_url,
                                    data=json.dumps(request_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)

        # expect the json reprisentation of the user to be returned
        response_data = response.json
        self.assertEqual(response_data['user_id'], self.user_id)
        self.assertEqual(response_data['ingredient_id'], request_data['ingredient_id'])
        self.assertEqual(response_data['coefficient'], request_data['coefficient'])

    @mock.patch('eggsnspam.oop_phrasebook.daos.UserPreferenceDao.get_by_user_ingredient')
    def test_get_user_preference(self, m_get_by_user_ingredient):
        """It lists all the users in the database"""

        # expect 404 if user's ingredient preference does not exist
        m_get_by_user_ingredient.return_value = None
        response = self.client.get(self.detail_url_template.format(user_id=1, ingredient_id=-1),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 404)

        # expect to get a json object representation of a user preference
        m_get_by_user_ingredient.return_value = {'id': 1, 'user_id': 1, 'ingredient_id': 4, 'coefficient': 0.8}
        response = self.client.get(self.detail_url_template.format(user_id=1, ingredient_id=4),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)

    @mock.patch('eggsnspam.oop_phrasebook.daos.UserPreferenceDao.update')
    @mock.patch('eggsnspam.oop_phrasebook.daos.UserPreferenceDao.get_by_user_ingredient')
    def test_update_user_preference(self, m_get_by_user_ingredient, m_update):
        """It updates a user preference in the database"""

        # expect 404 if user does not exist
        m_get_by_user_ingredient.return_value = None
        response = self.client.put(self.detail_url_template.format(user_id=0, ingredient_id=0),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 404)

        request_data = {
            "coefficient": .9
        }

        # expect a json representation of the updated user to be returned
        m_get_by_user_ingredient.return_value = {'id': 1, 'user_id': 1, 'ingredient_id': 4, 'coefficient': 0.8}
        m_update.return_value = True
        response = self.client.put(self.detail_url_template.format(user_id=1, ingredient_id=4),
                                   content_type='application/json',
                                   data=json.dumps(request_data))
        self.assertEqual(response.status_code, 200)
        response_data = response.json
        self.assertEqual(response_data['coefficient'], request_data['coefficient'])

    @mock.patch('eggsnspam.oop_phrasebook.daos.UserPreferenceDao.delete')
    @mock.patch('eggsnspam.oop_phrasebook.daos.UserPreferenceDao.get_by_user_ingredient')
    def test_delete_user_preference(self, m_get_by_user_ingredient, m_delete):
        """It deletes a user record in the database"""

        # expect a 404 error if invalid data is provided
        m_get_by_user_ingredient.return_value = None
        response = self.client.delete("/oop_phrasebook/user/0/preference/0")
        self.assertEqual(response.status_code, 404)

        # expect an object to be deleted if it is found
        m_get_by_user_ingredient.return_value = {'id': 1, 'user_id': 1, 'ingredient_id': 4, 'coefficient': 0.8}
        m_delete.return_value = True
        response = self.client.delete(self.detail_url_template.format(user_id=1,
                                                                      ingredient_id=4))
        self.assertEqual(response.status_code, 204)
