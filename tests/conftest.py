import pytest


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "record_mode": "new_episodes",
        "match_on": [
            "host",
            "port",
            "path",
            "body",
        ],
        "filter_headers": [("authorization", "DUMMY")],
    }
