import json

from .factories.oop_orm_factories import (BreakfastFactory, IngredientFactory, UserFactory,
                                         UserPreferenceFactory, BreakfastIngredientFactory)

from eggsnspam.extensions import db
from eggsnspam.oop_orm import models

from . import BaseTestCase
from .mixins import HealthViewTestCaseMixin, OrmTestCase
from .utils import AssertNumQueries


class HealthViewTestCase(HealthViewTestCaseMixin, BaseTestCase):
    """Testcase for healthcheck endpoint"""

    base_url_path = '/oop_orm'


class BreakfastTestCase(OrmTestCase, BaseTestCase):

    def test_list_breakfasts(self):
        """It lists all the breakfasts in the database"""

        # expect no breakfasts to return an empty json object
        response = self.client.get("/oop_orm/breakfast/",
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json
        self.assertIn("breakfasts", response_data)
        self.assertEqual(len(response_data["breakfasts"]), 0)

        # create 3 breakfasts
        breakfast_ids = []
        for i in range(3):
            breakfast_ids.append(BreakfastFactory().id)

        # exepect 3 breakfast objects to be returned
        response = self.client.get("/oop_orm/breakfast/",
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json
        for breakfast in response_data['breakfasts']:
            self.assertIn(breakfast['id'], breakfast_ids)

    def test_get_breakfast(self):
        """It gets a breakfast object in the database"""

        # expect a 404 to be returned if no breakfast is found
        response = self.client.get("/oop_orm/breakfast/-1",
                                   content_type='application/json')
        self.assertEqual(response.status_code, 404)

        breakfast = BreakfastFactory(name="eggs")

        response = self.client.get("/oop_orm/breakfast/{}".format(breakfast.id),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json
        self.assertEqual(breakfast.name, response_data['name'])
        self.assertEqual(breakfast.id, response_data['id'])


class IngredientTestCase(OrmTestCase, BaseTestCase):

    def test_list_breakfasts(self):
        """It lists all the breakfasts in the database"""

        # expect no breakfasts to return an empty json object
        response = self.client.get("/oop_orm/ingredient/",
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json
        self.assertIn("ingredients", response_data)
        self.assertEqual(len(response_data["ingredients"]), 0)

        # create 3 ingredients
        ingredient_ids = []
        for i in range(3):
            ingredient_ids.append(IngredientFactory().id)

        # exepect 3 ingredient objects to be returned
        response = self.client.get("/oop_orm/ingredient/",
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json
        for ingredient in response_data['ingredients']:
            self.assertIn(ingredient['id'], ingredient_ids)

    def test_get_ingredient(self):
        """It gets a ingredient object in the database"""

        # expect a 404 to be returned if no ingredient is found
        response = self.client.get("/oop_orm/ingredient/-1",
                                   content_type='application/json')
        self.assertEqual(response.status_code, 404)

        ingredient = IngredientFactory(name="spam")

        response = self.client.get("/oop_orm/ingredient/{}".format(ingredient.id),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json
        self.assertEqual(ingredient.name, response_data['name'])
        self.assertEqual(ingredient.id, response_data['id'])


class UserTestCase(OrmTestCase, BaseTestCase):

    def test_list_users(self):
        """It lists all the users in the database"""

        # expect no users to return an empty json object
        response = self.client.get("/oop_orm/user/",
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json
        self.assertIn("users", response_data)
        self.assertEqual(len(response_data["users"]), 0)

        # create 3 users
        user_ids = []
        for i in range(3):
            user_ids.append(UserFactory().id)

        # exepect 3 user objects to be returned
        response = self.client.get("/oop_orm/user/",
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json
        for user in response_data['users']:
            self.assertIn(user['id'], user_ids)

    def test_create_user(self):
        """It creates a user record in the database"""

        # expect a 400 error if invalid data is provided
        response = self.client.post("/oop_orm/user/",
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

        request_data = {
            "first_name": "Harrison",
            "last_name": "Ford"
        }

        # expect a 201 response if we created an object
        response = self.client.post("/oop_orm/user/",
                                    data=json.dumps(request_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)

        # expect the json reprisentation of the user to be returned
        response_data = response.json
        self.assertEqual(response_data['first_name'], request_data['first_name'])
        self.assertEqual(response_data['last_name'], request_data['last_name'])

        # expect the object to exist and have the correct data
        user = models.User.query.order_by(models.User.id.desc()).first()
        self.assertEqual(user.first_name, request_data['first_name'])
        self.assertEqual(user.last_name, request_data['last_name'])
        self.assertEqual(user.id, response_data['id'])

    def test_delete_user(self):
        """It deletes a user record in the database"""

        # expect a 404 error if invalid data is provided
        response = self.client.delete("/oop_orm/user/-1")
        self.assertEqual(response.status_code, 404)

        user = UserFactory(first_name="Alpha",
                           last_name="Ardvark")

        # expect an object to be deleted if it is found
        response = self.client.delete("/oop_orm/user/{}".format(user.id))
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(db.session.query(models.User).filter_by(id=user.id).scalar())

    def test_get_user(self):
        """It lists all the users in the database"""

        # expect to get a 404 response if no user found for ID
        response = self.client.get("/oop_orm/user/-1",
                                   content_type='application/json')
        self.assertEqual(response.status_code, 404)

        # expect to get a json object representation of a user to be returned
        user = UserFactory()
        response = self.client.get("/oop_orm/user/{}".format(user.id),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json
        self.assertEqual(response_data['id'], user.id)
        self.assertEqual(response_data['first_name'], user.first_name)
        self.assertEqual(response_data['last_name'], user.last_name)

    def test_update_user(self):
        """It updates a user in the database"""

        user = UserFactory(first_name="Alpha",
                           last_name="Ardvark")
        request_data = {
            "first_name": "Beta",
            "last_name": "Baboon"
        }

        # expect to get a 404 response if no user found for ID
        response = self.client.put("/oop_orm/user/-1",
                                   content_type='application/json')
        self.assertEqual(response.status_code, 404)

        # expect a json representation of the updated user to be returned
        response = self.client.put("/oop_orm/user/{}".format(user.id),
                                   content_type='application/json',
                                   data=json.dumps(request_data))
        self.assertEqual(response.status_code, 200)
        response_data = response.json
        self.assertEqual(response_data['first_name'], 'Beta')
        self.assertEqual(response_data['last_name'], 'Baboon')

        # expect the record to be updated
        user = models.User.query.get(user.id)
        self.assertEqual(user.first_name, request_data['first_name'])
        self.assertEqual(user.last_name, request_data['last_name'])

    def test_breakfast_recommendations(self):
        """It returns the recommended breakfasts for a user"""
        breakfasts = []
        for i in range(3):
            breakfasts.append(BreakfastFactory())

        ingredients = []
        for i in range(3):
            ingredients.append(IngredientFactory())

        user = UserFactory()

        breakfast_ingredients = (
            (breakfasts[0], ingredients[0], 0.8),
            (breakfasts[0], ingredients[1], 0.8),
            (breakfasts[0], ingredients[2], 0.2),
            (breakfasts[1], ingredients[0], 0.0),
            (breakfasts[1], ingredients[1], 0.2),
            (breakfasts[1], ingredients[2], 0.9),
            (breakfasts[2], ingredients[0], 0.9),
            (breakfasts[2], ingredients[1], 0.5),
            (breakfasts[2], ingredients[2], 0.1),
        )

        for breakfast, ingredient, coefficient in breakfast_ingredients:
            BreakfastIngredientFactory(breakfast=breakfast,
                                       ingredient=ingredient,
                                       coefficient=coefficient)

        ingredient_preferences = (
            (ingredients[0], 0.8),
            (ingredients[1], 0.4),
            (ingredients[2], 0.6),
        )

        for ingredient, coefficient in ingredient_preferences:
            UserPreferenceFactory(user=user,
                                  ingredient=ingredient,
                                  coefficient=coefficient)

        # We have to create the URL outside the context manager because user.id can trigger a query itself
        url = "/oop_orm/user/%d/breakfast_recommendations" % user.id
        with AssertNumQueries(db.session, 2):
            response = self.client.get(url, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        response_data = response.json
        self.assertIn('breakfast_recs', response_data)
        self.assertEqual(len(response_data['breakfast_recs']), 3)
        self.assertTrue('breakfast_id' in response_data['breakfast_recs'][0])
        self.assertTrue('score' in response_data['breakfast_recs'][0])


class UserPreferencesTestCase(OrmTestCase, BaseTestCase):

    list_url_template = "/oop_orm/user/{user_id}/preference/"
    detail_url_template = "/oop_orm/user/{user_id}/preference/{ingredient_id}"

    def setUp(self):
        super(UserPreferencesTestCase, self).setUp()

        # create a user for each test
        self.user = UserFactory()
        self.list_url = self.list_url_template.format(user_id=self.user.id)

    def test_list_user_preferences(self):
        """It lists all the user preferences in the database"""

        # expect 404 if user does not exist
        response = self.client.get(self.list_url_template.format(user_id=0), content_type='application/json')
        self.assertEqual(response.status_code, 404)

        # expect no user preferences to return an empty json object
        response = self.client.get(self.list_url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json
        self.assertIn("user_preferences", response_data)
        self.assertEqual(len(response_data["user_preferences"]), 0)

        # create 3 user preferences
        for i in range(3):
            UserPreferenceFactory.create(user=self.user)

        # exepect 3 objects to be returned
        response = self.client.get(self.list_url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json
        self.assertIn("user_preferences", response_data)
        self.assertEqual(len(response_data["user_preferences"]), 3)

    def test_create_user_preference(self):
        """It creates a user preference record in the database"""

        # expect 404 if user does not exist
        response = self.client.post(self.list_url_template.format(user_id=0), content_type='application/json')
        self.assertEqual(response.status_code, 404)

        # expect a 400 error if invalid data is provided
        response = self.client.post(self.list_url, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # create an ingredient
        ingredient_id = IngredientFactory().id

        request_data = {
            "ingredient": ingredient_id,
            "coefficient": 0.5
        }

        # expect a 201 response if we created an object
        response = self.client.post(self.list_url,
                                    data=json.dumps(request_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)

        # expect the json reprisentation of the user to be returned
        response_data = response.json
        self.assertEqual(response_data['user_id'], self.user.id)
        self.assertEqual(response_data['ingredient_id'], request_data['ingredient'])
        self.assertEqual(response_data['coefficient'], request_data['coefficient'])

        # expect the object to exist and have the correct data
        user_preference = models.UserPreference.query.get((self.user.id, ingredient_id))
        self.assertEqual(user_preference.user_id, self.user.id)
        self.assertEqual(user_preference.ingredient_id, request_data['ingredient'])
        self.assertEqual(user_preference.coefficient, request_data['coefficient'])

    def test_create_duplicate_user_preference(self):
        """It prevents creating a duplicate user preference"""

        # create an ingredient
        ingredient_id = IngredientFactory().id

        request_data = {
            "ingredient": ingredient_id,
            "coefficient": 0.5
        }

        # expect a 201 response for the first attempt
        response = self.client.post(self.list_url,
                                    data=json.dumps(request_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)

        # expect a 201 response if we created an object
        response = self.client.post(self.list_url,
                                    data=json.dumps(request_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_get_user_preference(self):
        """It lists all the users in the database"""

        # expect 404 if user does not exist
        response = self.client.get(self.detail_url_template.format(user_id=0, ingredient_id=0),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 404)

        # expect 404 if user's ingredient preference does not exist
        response = self.client.get(self.detail_url_template.format(user_id=self.user.id, ingredient_id=0),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 404)

        ingredient = IngredientFactory.create()
        UserPreferenceFactory.create(user=self.user, ingredient=ingredient)

        # expect to get a json object representation of a user preference
        response = self.client.get(self.detail_url_template.format(user_id=self.user.id, ingredient_id=ingredient.id),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_update_user_preference(self):
        """It updates a user preference in the database"""

        # expect 404 if user does not exist
        response = self.client.get(self.detail_url_template.format(user_id=0, ingredient_id=0),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 404)

        ingredient = IngredientFactory.create()
        UserPreferenceFactory.create(user=self.user, ingredient=ingredient, coefficient=.2)
        db.session.flush()

        request_data = {
            "coefficient": .9
        }

        # expect a json representation of the updated user to be returned
        response = self.client.put(self.detail_url_template.format(user_id=self.user.id, ingredient_id=ingredient.id),
                                   content_type='application/json',
                                   data=json.dumps(request_data))
        self.assertEqual(response.status_code, 200)
        response_data = response.json
        self.assertEqual(response_data['coefficient'], request_data['coefficient'])

        # expect the record to be updated
        user_preference = models.UserPreference.query.get((self.user.id, ingredient.id))
        self.assertEqual(user_preference.coefficient, request_data['coefficient'])

    def test_delete_user_preference(self):
        """It deletes a user record in the database"""

        # expect a 404 error if invalid data is provided
        response = self.client.delete("/oop_orm/user/0/preference/0")
        self.assertEqual(response.status_code, 404)

        user_preference = UserPreferenceFactory.create(user=self.user, coefficient=.2)
        db.session.flush()

        # expect an object to be deleted if it is found
        response = self.client.delete(self.detail_url_template.format(user_id=self.user.id,
                                                                      ingredient_id=user_preference.ingredient_id))
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(db.session.query(models.UserPreference).get(
            (self.user.id, user_preference.ingredient_id)))
