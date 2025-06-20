import pytest


@pytest.fixture(scope="session")
def vcr_config():
    return {
        "record_mode": "new_episodes",
        "match_on": [
            "body", #  To match the prompt
            "host", #  If you want a new recording when changing the LLM service (e.g., openai to gemini)
        ],
        "filter_headers": [("authorization", "DUMMY")],
    }
