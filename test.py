import unittest
from unittest import mock

from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


class MyTestCase(unittest.TestCase):
    @mock.patch("Service.ServiceInterface.ServiceInterface.getAll")
    def test_1_get_all(self, mock_get_all):
        mock_get_all.return_value = []
        response = client.get("/items")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    @mock.patch("Repository.RepositoryInterface.RepositoryInterface.addEntity")
    @mock.patch("Repository.RepositoryInterface.RepositoryInterface.getEntity")
    def test_2_add_movie(self, mock_add_movie, mock_get_movie):
        mock_add_movie.return_value = {"message": "123e4567-e89b-12d3-a456-426614174000 added successfully"}
        mock_get_movie.return_value = {"movieId": "123e4567-e89b-12d3-a456-426614174000",
                                       "title": "Movie",
                                       "year": 2021,
                                       "genre": "Action"}
        response = client.post("/items",
                               json={"movieId": "123e4567-e89b-12d3-a456-426614174000",
                                     "title": "Movie",
                                     "year": 2021,
                                     "genre": "Action"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "123e4567-e89b-12d3-a456-426614174000 added successfully"})
        response = client.get("/items")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {"id": "123e4567-e89b-12d3-a456-426614174000", "title": "Movie", "year": 2021, "genre": "Action"}])

    @mock.patch("Repository.RepositoryInterface.RepositoryInterface.getEntity")
    def test_3_get_movie(self, mock_get_movie):
        mock_get_movie.return_value = {"movieId": "123e4567-e89b-12d3-a456-426614174000",
                                       "title": "Movie",
                                       "year": 2021,
                                       "genre": "Action"}
        response = client.get("/items/123e4567-e89b-12d3-a456-426614174000")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": "123e4567-e89b-12d3-a456-426614174000", "title": "Movie", "year": 2021, "genre": "Action"})

    @mock.patch("Repository.RepositoryInterface.RepositoryInterface.updateEntity")
    @mock.patch("Repository.RepositoryInterface.RepositoryInterface.getEntity")
    def test_4_update_movie(self, mock_update_movie, mock_get_movie):
        mock_update_movie.return_value = {"message": "123e4567-e89b-12d3-a456-426614174000 updated successfully"}
        mock_get_movie.return_value = {"movieId": "123e4567-e89b-12d3-a456-426614174000",
                                       "title": "UpdatedMovie",
                                       "year": 2022,
                                       "genre": "Drama"}
        response = client.put("/items/123e4567-e89b-12d3-a456-426614174000",
                              json={"movieId": "123e4567-e89b-12d3-a456-426614174000",
                                     "title": "UpdatedMovie",
                                     "year": 2022,
                                     "genre": "Drama"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "123e4567-e89b-12d3-a456-426614174000 updated successfully"})
        response = client.get("/items/123e4567-e89b-12d3-a456-426614174000")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": "123e4567-e89b-12d3-a456-426614174000", "title": "UpdatedMovie", "year": 2022, "genre": "Drama"})

    @mock.patch("Repository.RepositoryInterface.RepositoryInterface.deleteEntity")
    @mock.patch("Repository.RepositoryInterface.RepositoryInterface.getEntity")
    def test_5_delete_movie(self, mock_delete_movie, mock_get_movie):
        response = client.delete("/items/123e4567-e89b-12d3-a456-426614174000")
        self.assertEqual(response.status_code, 204)
        response = client.get("/items/123e4567-e89b-12d3-a456-426614174000")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Item not found."})


if __name__ == '__main__':
    unittest.main()
