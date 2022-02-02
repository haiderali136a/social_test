import pytest
from rest_framework.reverse import reverse
from tests.conftest import test_signup_payload, test_password, signup_url


@pytest.mark.django_db
def test_create_user(client, test_signup_payload, signup_url):
    resp = client.post(signup_url, data=test_signup_payload)
    assert "email" in resp.json()
    assert resp.status_code == 201


@pytest.mark.django_db
def test_login_user(client, test_signup_payload, signup_url):
    resp = client.post(signup_url, data=test_signup_payload)
    url = reverse('token_obtain_pair')
    payload = {"email": "someone@gmail.com", "password": test_password}
    response = client.post(url, data=payload)
    assert response.status_code == 200
    assert 'access' in response.json()
