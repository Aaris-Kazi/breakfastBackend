from django.test import TestCase

# Create your tests here.


class HealthCase(TestCase):

    def test_checkHealth(self):
        for path in ("/health", "/health/"):
            with self.subTest(path=path):
                resp = self.client.get(
                    path,
                    HTTP_ORIGIN="http://localhost:5173",
                )

                self.assertEqual(resp.status_code, 200)
                self.assertEqual(
                    resp["Access-Control-Allow-Origin"],
                    "http://localhost:5173",
                )