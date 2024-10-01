from http import HTTPStatus

import pytest
from django.shortcuts import resolve_url
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_status_code(client):
    response = client.get(resolve_url("index"))
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_template(client):
    response = client.get(resolve_url("index"))
    assertTemplateUsed(response, "index.html")
