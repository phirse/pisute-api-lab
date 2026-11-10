import pytest

STARS_ERROR = "number of stars must be between 1 and 5 (inclusive)"


# Boundary values of an update: 1 and 5 stars are saved, 0 and 6 are refused,
# and a refused update leaves the rating as it was.
@pytest.mark.parametrize("stars, status", [(0, 400), (1, 200), (5, 200), (6, 400)])
def test_update_stars_at_the_boundaries(api, auth, rating, stars, status):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": stars}, headers=auth)
    assert res.status_code == status
    if status == 200:
        assert res.json()["stars"] == stars
        expected = stars
    else:
        assert res.json() == {"error": STARS_ERROR}
        expected = rating["stars"]
    res = api.get(path, headers=auth)
    assert res.status_code == 200
    assert res.json()["stars"] == expected
