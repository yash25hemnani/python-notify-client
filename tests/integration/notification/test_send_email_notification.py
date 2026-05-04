import pytest
import logging
import os
from conftest import (
    TEST_CUSTOMER_ID,
    TEST_CUSTOMER_EMAIL,
    TEST_TEMPLATE_SLUG,
    TEST_NOTIFICATION_DATA,
    TEST_FILE_PATHS,
    TEST_UPLOAD_FILES,
    TEST_CC_EMAILS,
    TEST_BCC_EMAILS,
    _log_api_response,
    _log_api_error,
    _assert_success_response_format,
    _assert_message,
)

logger = logging.getLogger(__name__)


def _assert_send_email_notification_response(response: dict) -> None:
    _assert_success_response_format(response=response)

    message = _assert_message(
        response=response,
        message_tuple=("Email notification queued",),
    )

    logger.info("Email notification status: %s", message)


@pytest.mark.integration
def test_send_email_notification(notification_engine):
    try:

        files = []

        for file_path in TEST_UPLOAD_FILES:
            files.append(
                (
                    "files",  # Expected by node backend
                    (
                        os.path.basename(file_path),
                        open(file_path, "rb"),
                        "application/pdf",
                    ),
                )
            )

        response = notification_engine.send_email_notification(
            customer_id=TEST_CUSTOMER_ID,
            customer_email=TEST_CUSTOMER_EMAIL,
            template_slug=TEST_TEMPLATE_SLUG,
            data=TEST_NOTIFICATION_DATA,
            cc=TEST_CC_EMAILS,
            bcc=TEST_BCC_EMAILS,
            file_paths=TEST_FILE_PATHS,
            files=files,
        )

        _log_api_response(response=response)

        assert response is not None, "Expected a non-null response"
        _assert_send_email_notification_response(response)

    except Exception as e:
        _log_api_error(e)
        pytest.fail(f"API request failed: {e}")
