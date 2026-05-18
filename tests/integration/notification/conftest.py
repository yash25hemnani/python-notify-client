import pytest
import logging
from notification_sdk.client import ApiClient
from notification_sdk.notifications import NotificationEngine
from notification_sdk.env import ENV
import json
import os

logger = logging.getLogger(__name__)

_test_data_path = os.path.join(os.path.dirname(__file__), "..", "test_data.json")

with open(_test_data_path) as f:
    _test_data = json.load(f)

# ── Customer ──────────────────────────────────────────────────────────────────
TEST_CUSTOMER_ID = _test_data["test_customer_id"]
TEST_CUSTOMER_EMAIL = _test_data["test_customer_email"]
TEST_CC_EMAILS = _test_data["test_cc_emails"]
TEST_BCC_EMAILS = _test_data["test_bcc_emails"]
TEST_SUBSCRIPTION = _test_data["subscription"]
TEST_NOTIFICATION_DATA = _test_data["test_notification_data"]
TEST_FILE_PATHS = _test_data["test_file_paths"]
TEST_UPLOAD_FILES = _test_data["test_upload_files"]
TEST_TEMPLATE_SLUG = "hello-ops-walo"


# ── Fixtures ──────────────────────────────────────────────────────────────────
@pytest.fixture(scope="module")
def notification_engine():
    client = ApiClient()
    return NotificationEngine(client=client)


# ── Logging Helpers ───────────────────────────────────────────────────────────
def _log_api_response(response: dict) -> None:
    """Logs a successful API response."""
    logger.info("--- API SUCCESS RESPONSE ---")
    logger.info("Response: %s", response)


def _log_api_error(e: Exception) -> None:
    """Logs a failed API response."""
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


# ── Assertion Helpers ─────────────────────────────────────────────────────────
def _assert_success_response_format(response: dict) -> None:
    """
    Asserts the standard success response shape:
    {
        "success": True,
        "data": { ... }
    }
    """
    assert response.get("success") is True, f"Expected success=True, got: {response}"
    assert "data" in response, f"Expected 'data' key in response, got: {response}"


def _assert_message(response: dict, message_tuple: tuple = ()) -> str:
    """
    Asserts response message is one of the expected values.

    Args:
        response: Parsed API response dict.
        message_tuple: Tuple of acceptable message strings. Skip assertion if empty.

    Returns:
        The message string from the response.
    """
    message = response["data"].get("message")

    if message_tuple:
        assert message in message_tuple, f"Unexpected message: {message}"

    logger.info("Response message: %s", message)
    return message
