import pytest

STARS_ERROR = "number of stars must be between 1 and 5 (inclusive)"
DECIMAL_ERROR = (
    "json: cannot unmarshal number 3.5 into Go struct field Rating.stars of type int"
)
TEXT_ERROR = "json: cannot unmarshal string into Go struct field Rating.stars of type int"
AUTH_ERROR = "authentication failed"
UNKNOWN_PIZZA = 999999999


# Base choice: 3 stars as a whole number, a real pizza, the user's token.
def test_base_choice_is_saved(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 201
    assert res.json()["stars"] == 3
    assert res.json()["pizza_id"] == pizza_id


# C1: a number of stars below 1 or above 5 is refused with a message.
@pytest.mark.parametrize("stars", [0, 6])
def test_stars_out_of_range(api, auth, pizza_id, stars):
    new = {"pizza_id": pizza_id, "stars": stars}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": STARS_ERROR}


# C2: a decimal number of stars is refused with a message.
def test_decimal_stars_are_refused(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3.5}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": DECIMAL_ERROR}


# C2: stars sent as text are refused with a message.
def test_text_stars_are_refused(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": "3"}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": TEXT_ERROR}


# C2: a rating without the stars field is refused with a message.
def test_missing_stars_are_refused(api, auth, pizza_id):
    new = {"pizza_id": pizza_id}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": STARS_ERROR}


# C3: a rating of a pizza that does not exist is refused with a message.
def test_unknown_pizza_is_refused(api, auth):
    new = {"pizza_id": UNKNOWN_PIZZA, "stars": 3}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": f"pizza ID {UNKNOWN_PIZZA} not found"}


# C4: a rating without a token is refused with 401 and a message.
def test_rating_without_token_is_refused(api, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    res = api.post("/api/ratings", json=new)
    assert res.status_code == 401
    assert res.json() == {"error": AUTH_ERROR}


# C4: a token of the wrong length is refused with 401 and a message.
def test_rating_with_short_token_is_refused(api, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    short = {"Authorization": "token short"}
    res = api.post("/api/ratings", json=new, headers=short)
    assert res.status_code == 401
    assert res.json() == {"error": AUTH_ERROR}
