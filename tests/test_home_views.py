from . import BaseTestCase


class HomeTestCase(BaseTestCase):

    def test_index(self):
        """It says hello properly"""
        response = self.client.get("/", content_type='text/plain')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Hello world!", response.data)
