import json

import pytest
from fixtures import user_token


@pytest.mark.django_db
def test_ads_create(client, user, category):
    response = client.post(
        "/ads/create/",
        {
            "name": "new test ad",
            "price": 10,
            "description": "test description",
            "is_published": False,
            "author": user.id,
            "category": category.id
        },
        content_type="application/json")

    assert response.status_code == 201
    print("TEST RESP   ", json.loads(response.content) )
    assert json.loads(response.content) == {
        'id': 1,
        'author': user.id,
        'category': category.id,
        'description': 'test description',
        'image': None,
        'is_published': False,
        'name': 'new test ad',
        'price': 10,
    }
