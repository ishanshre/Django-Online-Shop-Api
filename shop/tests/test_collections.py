"""Test using pytest"""
from rest_framework.test import APIClient
from rest_framework import status

import pytest

@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonymous_returns_401(self):
        # AAA (Arrange, Act, Assert)

        # Arrange

        #Act
        self.client = APIClient()
        response = self.client.post("/collections/", {"title":"a"})

        #Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
