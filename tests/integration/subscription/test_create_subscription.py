import pytest
import logging
from conftest import (
    TEST_CUSTOMER_ID,
    TEST_CUSTOMER_EMAIL,
    TEST_SUBSCRIPTION,
    _log_api_response,
    _log_api_error,
    _assert_success_response_format,
    _assert_messages,
)

logger = logging.getLogger(__name__)


def _assert_create_subscription_response(response: dict) -> None:
    _assert_success_response_format(response=response)

    message = _assert_messages(response=response, message_tuple=("Subscription created successfully",
        "Subscription already exists"))
    
    logger.info("Subscription status: %s", message)


@pytest.mark.integration
def test_create_subscription(engine):
    try:
        response = engine.create_subscription(
            customer_id=TEST_CUSTOMER_ID,
            customer_email=TEST_CUSTOMER_EMAIL,
            subscription=TEST_SUBSCRIPTION,
        )

        _log_api_response(response=response)
        

        assert response is not None, "Expected a non-null response"
        _assert_create_subscription_response(response)

    except Exception as e:
        _log_api_error(e)
        pytest.fail(f"API request failed: {e}")