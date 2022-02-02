import pytest
from rest_framework.reverse import reverse


@pytest.fixture
def test_password():
    return 'abcde12345hj'


@pytest.fixture
def signup_url():
    return reverse('signup')


@pytest.fixture
def test_signup_payload():
    payload = {
        'username': 'someone',
        'email': 'someone@gmail.com',
        'password': test_password,
        'first_name': 'Haider',
        'last_name': 'Ali'
    }
    return payload
