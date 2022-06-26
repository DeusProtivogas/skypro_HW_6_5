import pytest

from ads.serializers import AdDetailSerializer
from fixtures import user_token


@pytest.mark.django_db
def test_ads_create(client, ad, user_token):
    response = client.get(
        f"/ads/{ad.id}/",
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {user_token}")

    assert response.status_code == 200
    assert response.data == AdDetailSerializer(ad).data
