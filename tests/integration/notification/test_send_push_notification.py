import pytest
import logging
from conftest import (
    TEST_CUSTOMER_ID,
    TEST_CUSTOMER_EMAIL,
    TEST_TEMPLATE_SLUG,
    TEST_NOTIFICATION_DATA,
    _log_api_response,
    _log_api_error,
    _assert_success_response_format,
    _assert_message,
)

logger = logging.getLogger(__name__)


def _assert_send_push_notification_response(response: dict) -> None:
    _assert_success_response_format(response=response)

    message = _assert_message(
        response=response,
        message_tuple=("Push notifications queued",),
    )

    logger.info("Push notification status: %s", message)


@pytest.mark.integration
def test_send_push_notification(notification_engine):
    try:
        response = notification_engine.send_push_notification(
            customer_id=TEST_CUSTOMER_ID,
            customer_email=TEST_CUSTOMER_EMAIL,
            template_slug=TEST_TEMPLATE_SLUG,
            data=TEST_NOTIFICATION_DATA,
        )

        _log_api_response(response=response)

        assert response is not None, "Expected a non-null response"
        _assert_send_push_notification_response(response)

    except Exception as e:
        _log_api_error(e)
        pytest.fail(f"API request failed: {e}")