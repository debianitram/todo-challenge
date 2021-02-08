import json

from rest_framework.test import APIClient


JSON_CONTENT_TYPE = "application/json"


def get_authenticated_client(user=None):
    client = APIClient()
    if user is not None:
        client.force_authenticate(user=user)
    return client


def get(url, params=None, headers=None, user_logged=None):
    url += "?{}".format(params) if params else ''
    client = get_authenticated_client(user_logged)
    if headers is None:
        headers = {'HTTP_ACCEPT': JSON_CONTENT_TYPE}

    response = client.get(url, **headers)
    return response


def post(url, data=None, headers=None, user_logged=None):
    url = url + '/' if not url.endswith('/') else url
    client = get_authenticated_client(user_logged)
    if headers is None:
        headers = {'HTTP_ACCEPT': JSON_CONTENT_TYPE}

    response = client.post(url, data=json.dumps(data), content_type=JSON_CONTENT_TYPE, **headers)
    return response


def patch(url, data=None, headers=None, user_logged=None):
    url = url + '/' if not url.endswith('/') else url
    client = get_authenticated_client(user_logged)
    if headers is None:
        headers = {'HTTP_ACCEPT': JSON_CONTENT_TYPE}

    response = client.patch(url, data=json.dumps(data), content_type=JSON_CONTENT_TYPE, **headers)
    return response


def delete(url, headers=None, user_logged=None):
    url = url + '/' if not url.endswith('/') else url
    client = get_authenticated_client(user_logged)
    if headers is None:
        headers = {'HTTP_ACCEPT': JSON_CONTENT_TYPE}

    response = client.delete(url, content_type=JSON_CONTENT_TYPE, **headers)
    return response
