import unittest
from app import app


class TaskFlowTest(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_add_page(self):
        response = self.client.get("/add")
        self.assertEqual(response.status_code, 200)

    def test_create_task(self):
        response = self.client.post(
            "/add",
            data={
                "title": "Estudar Flask",
                "description": "Criar CRUD",
                "priority": "Alta"
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Estudar Flask", response.data)


if __name__ == "__main__":
    unittest.main()