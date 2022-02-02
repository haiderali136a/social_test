import pytest
from django.urls import reverse
from tests.conftest import test_password, test_signup_payload


@pytest.mark.django_db
def test_newsfeed(client):
    url = reverse('all-posts')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_post_unauthorized(client):
    create_post_url = reverse('create-post')
    res = client.post(create_post_url, data={'body': 'Hello there'})
    assert res.status_code == 401
