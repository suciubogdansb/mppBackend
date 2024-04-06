import unittest
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


class MyTestCase(unittest.TestCase):
    def test_1_get_all(self):
        response = client.get("/items")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_2_add_movie(self):
        response = client.post("/items",
                               json={"id": "123e4567-e89b-12d3-a456-426614174000",
                                     "title": "Movie",
                                     "year": 2021,
                                     "genre": "Action"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "123e4567-e89b-12d3-a456-426614174000 added successfully"})
        response = client.get("/items")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {"id": "123e4567-e89b-12d3-a456-426614174000", "title": "Movie", "year": 2021, "genre": "Action"}])

    def test_3_get_movie(self):
        response = client.get("/items/123e4567-e89b-12d3-a456-426614174000")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": "123e4567-e89b-12d3-a456-426614174000", "title": "Movie", "year": 2021, "genre": "Action"})

    def test_4_update_movie(self):
        response = client.put("/items/123e4567-e89b-12d3-a456-426614174000",
                              json={"id": "123e4567-e89b-12d3-a456-426614174000",
                                     "title": "UpdatedMovie",
                                     "year": 2022,
                                     "genre": "Drama"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "123e4567-e89b-12d3-a456-426614174000 updated successfully"})
        response = client.get("/items/123e4567-e89b-12d3-a456-426614174000")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": "123e4567-e89b-12d3-a456-426614174000", "title": "UpdatedMovie", "year": 2022, "genre": "Drama"})

    def test_5_delete_movie(self):
        response = client.delete("/items/123e4567-e89b-12d3-a456-426614174000")
        self.assertEqual(response.status_code, 204)
        response = client.get("/items/123e4567-e89b-12d3-a456-426614174000")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Item not found."})


if __name__ == '__main__':
    unittest.main()
