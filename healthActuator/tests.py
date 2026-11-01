from django.test import TestCase

# Create your tests here.


class HealthCase(TestCase):

    def test_checkHealth(self):
        resp = self.client.get("/health/")

        self.assertEqual(resp.status_code, 200)