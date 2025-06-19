import pytest


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "record_mode": "new_episodes",
        "match_on": [
            "method", # POST
            "scheme", # http
            "host",
            "port",
            "path",
            "query", # ?? TODO : à supprimer si pas pertinent
            "body",
        ],
        "filter_headers": [("authorization", "DUMMY")],
    }
