import pytest
import logging
from notification_sdk.client import ApiClient
from notification_sdk.subscriptions import SubscriptionEngine
from notification_sdk.env import ENV
import json
import os

logger = logging.getLogger(__name__)

_test_data_path = os.path.join(os.path.dirname(__file__), "..", "test_data.json")

with open(_test_data_path) as f:
    _test_data = json.load(f)

TEST_SUBSCRIPTION = _test_data["subscription"]

TEST_CUSTOMER_ID = _test_data["test_customer_id"]
TEST_CUSTOMER_EMAIL = _test_data["test_customer_email"]

@pytest.fixture(scope="module")
def engine():
    client = ApiClient()
    return SubscriptionEngine(client=client)

def _log_api_response(response: dict):
    logger.info("--- API SUCCESS RESPONSE ---")
    logger.info("Response: %s", response)

def _log_api_error(e: Exception) -> None:
    """
        Logs api error
    """
    response = getattr(e, "response", None)
    if response is None:
        logger.error("No response attached to exception: %s", e)
        return

    logger.error("--- API ERROR RESPONSE ---")
    logger.error("Status Code: %s", response.status_code)
    logger.error("Response Body: %s", response.text)

    try:
        body = response.json()
        logger.error("JSON: %s", body)

        error = body.get("error", {})
        logger.error("Error Code: %s", error.get("code"))
        logger.error("Error Message: %s", error.get("message"))
    except Exception:
        pass

def _assert_success_response_format(response:dict):
    """
    Checks if data attribute has the format - 
    data : {
        "success": boolean,
        "data": {}
    }
    """
    assert response.get("success") is True, f"Expected success=True, got: {response}"
    assert "data" in response, f"Expected 'data' key in response, got: {response}"

def _assert_messages(response:dict, message_tuple:tuple):
    message = response["data"].get("message")

    if not message_tuple:
        return message
    
    assert message in message_tuple, f"Unexpected message: {message}"

    return message