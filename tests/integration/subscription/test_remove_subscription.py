import pytest
import logging
from conftest import (
    TEST_SUBSCRIPTION,
    _log_api_response,
    _log_api_error,
    _assert_success_response_format,
    _assert_messages,
)

logger = logging.getLogger(__name__)


def _assert_remove_subscription_response(response: dict) -> None:
    _assert_success_response_format(response=response)

    message = _assert_messages(response=response, message_tuple=("Subscription removed successfully"))
    
    logger.info("Subscription status: %s", message)


@pytest.mark.integration
def test_remove_subscription(engine):
    try:
        response = engine.remove_subscription(
            endpoint=TEST_SUBSCRIPTION["endpoint"],
        )

        _log_api_response(response=response)
        

        assert response is not None, "Expected a non-null response"
        _assert_remove_subscription_response(response)

    except Exception as e:
        _log_api_error(e)
        pytest.fail(f"API request failed: {e}")