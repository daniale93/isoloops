from unittest.mock import patch
from search_youtube import search_many
import pandas as pd

# Sample mock response data
mock_response = {
    "items": [
        {
            "id": {"videoId": "abc123"},
            "snippet": {"title": "Sample Video 1"}
        },
        {
            "id": {"videoId": "xyz789"},
            "snippet": {"title": "Sample Video 2"}
        },
    ]
}

# Patch the requests.get method used inside search_youtube
@patch("search_youtube.requests.get")
def test_search_many(mock_get):
    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return mock_response

    mock_get.return_value = MockResponse()

    queries = ["fela kuti", "tito puente", "os mutantes"]
    df = search_many(queries, max_results=2)

    print(df)

# Run the test
if __name__ == "__main__":
    test_search_many()