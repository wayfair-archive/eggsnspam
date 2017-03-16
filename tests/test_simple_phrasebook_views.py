import json

import mock

from . import BaseTestCase
from .mixins import PhrasebookFixturedTestCase


class BreakfastTestCase(PhrasebookFixturedTestCase, BaseTestCase):

    @mock.patch('eggsnspam.simple_phrasebook.daos.BreakfastRecsDao.get_ingredient_preferences')
    @mock.patch('eggsnspam.simple_phrasebook.daos.BreakfastRecsDao.get_all_breakfast_ingredients')
    def test_breakfast_recommendations(self, m_get_all_breakfast_ingredients, m_get_ingredient_preferences):
        """It returns the recommended breakfasts for a user"""
        m_get_all_breakfast_ingredients.return_value = [
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

        m_get_ingredient_preferences.return_value = [
            {'ingredient_id': 1, 'coefficient': 0.8},
            {'ingredient_id': 2, 'coefficient': 0.4},
            {'ingredient_id': 3, 'coefficient': 0.6}
        ]

        response = self.client.get("/simple_phrasebook/user/1/breakfast_recommendations",
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn('breakfast_recs', response_data)
        self.assertEqual(len(response_data['breakfast_recs']), 3)
        self.assertTrue('breakfast_id' in response_data['breakfast_recs'][0])
        self.assertTrue('score' in response_data['breakfast_recs'][0])
