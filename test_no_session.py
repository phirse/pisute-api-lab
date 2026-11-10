import uuid

import requests

SITE = "https://quickpizza.grafana.com"


# The steps of log_in_new_user, with every request on its own.
def test_log_in_without_a_session():
    name = "lab-" + uuid.uuid4().hex[:12]
    user = {"username": name, "password": "Pizza-2026"}
    res = requests.post(SITE + "/api/users", json=user)
    assert res.status_code == 201
    res = requests.post(SITE + "/api/users/token/login", json=user)
    assert res.status_code == 200
