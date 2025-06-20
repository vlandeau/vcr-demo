import pytest


@pytest.fixture(scope="session")
def vcr_config():
    return {
        "record_mode": "new_episodes",
        "match_on": [
            "host", #  If you want a new recording when changing the LLM service (e.g., openai to gemini)
            "body", #  To match the prompt
        ],
        "filter_headers": [("authorization", "DUMMY")],
    }
