# Notification SDK User Manual

This user manual describes how to install, configure, and use the Python Notification SDK included in this repository.

## Overview

The SDK provides a thin client wrapper for a notification API. It supports:

- email notifications with optional attachments
- push notifications with template data
- push subscription management (create, retrieve, remove)
- payload conversion from Python `snake_case` names to API-friendly `camelCase`

The SDK is intentionally lightweight and designed to work with a REST API that expects a specific request format.

## Requirements

- Python 3.10+ (or compatible Python version)
- `requests`
- `python-dotenv`
- `pytest` for running tests

Install the dependencies with:

```bash
python -m pip install -r requirements.txt
```

## Configuration

The SDK reads configuration from environment variables. Use a `.env` file or set environment variables directly.

Required environment variables:

- `API_KEY` — API key for authorization
- `BASE_URL` — Base URL for the notification API
- `TEST_CUSTOMER_ID` — A customer identifier used by sample tests
- `TEST_CUSTOMER_EMAIL` — A test customer email used by sample tests

Example `.env`:

```text
API_KEY=your_api_key
BASE_URL=https://api.example.com
TEST_CUSTOMER_ID=123456789
TEST_CUSTOMER_EMAIL=test@example.com
```

## Package Layout

The SDK contains the following modules:

- `notification_sdk/client.py`
  - `ApiClient`
  - handles authenticated GET and POST requests
- `notification_sdk/env.py`
  - loads environment variables using `dotenv`
  - raises an error when required variables are missing
- `notification_sdk/notifications.py`
  - `NotificationEngine`
  - email and push notification APIs
- `notification_sdk/subscriptions.py`
  - `SubscriptionEngine`
  - subscription create/get/remove APIs
- `notification_sdk/utils.py`
  - `generate_payload()` and `generate_params()` helpers
  - converts payload keys from `snake_case` to `camelCase`

## Core Components

### ApiClient

`ApiClient` is the HTTP client used by the notification and subscription engines.

Constructor:

```python
client = ApiClient()
```

Methods:

- `get(endpoint: str, params: dict = None)` — sends a GET request
- `post(endpoint: str, data=None, files=None)` — sends a POST request

The client automatically adds:

- `x-api-key` header with the API key
- `Accept: application/json`

### NotificationEngine

`NotificationEngine` exposes notification-specific API calls.

Constructor:

```python
from notification_sdk.notifications import NotificationEngine
engine = NotificationEngine(client=client)
```

Methods:

- `upload_email_attachments(files: list) -> list`
  - uploads attachments and returns file path metadata
- `send_email_notification(...) -> dict`
  - sends an email notification
- `send_push_notification(...) -> dict`
  - sends a push notification

#### Email notification parameters

- `customer_id: str`
- `customer_email: str`
- `template_slug: str`
- `data: Any` (optional dynamic template data)
- `cc: list` (optional list of CC email addresses)
- `bcc: list` (optional list of BCC email addresses)
- `reply_to: str` (optional reply-to address)
- `files: list` (optional list of files to upload)
- `file_paths: list` (optional list of already uploaded file paths)

When `files` is provided, `send_email_notification()` uploads attachments via `/notification/notify/upload-attachments` before sending the email.

#### Push notification parameters

- `customer_id: str`
- `customer_email: str`
- `template_slug: str`
- `data: Any`

### SubscriptionEngine

`SubscriptionEngine` handles push subscription management.

Constructor:

```python
from notification_sdk.subscriptions import SubscriptionEngine
engine = SubscriptionEngine(client=client)
```

Methods:

- `create_subscription(customer_id: str, customer_email: str, subscription: Any) -> dict`
- `get_subscription(endpoint: str) -> dict`
- `remove_subscription(endpoint: str) -> dict`

The subscription payload is expected to match the API contract, for example:

```python
subscription = {
    "endpoint": "https://example.com/fcm/send/abc123",
    "keys": {
        "auth": "auth-token",
        "p256dh": "p256dh-key",
    },
}
```

## Payload Helpers

`notification_sdk.utils` provides two helpers:

- `generate_payload(**kwargs)`
  - converts keys from `snake_case` to `camelCase`
  - removes entries with `None` values
- `generate_params(**kwargs)`
  - converts query parameters to `camelCase`

These helpers ensure the SDK sends the expected naming style to the backend.

## Example Workflows

### Basic push notification

```python
from notification_sdk.client import ApiClient
from notification_sdk.notifications import NotificationEngine

client = ApiClient()
engine = NotificationEngine(client=client)

response = engine.send_push_notification(
    customer_id="123456789",
    customer_email="customer@example.com",
    template_slug="welcome-new-user",
    data={"name": "Jane"},
)
print(response)
```

### Email notification with attachments

```python
from notification_sdk.client import ApiClient
from notification_sdk.notifications import NotificationEngine

client = ApiClient()
engine = NotificationEngine(client=client)

files = [
    (
        "files",
        ("terms.pdf", open("terms.pdf", "rb"), "application/pdf"),
    ),
]

response = engine.send_email_notification(
    customer_id="123456789",
    customer_email="customer@example.com",
    template_slug="email-template",
    data={"customerName": "Jane"},
    files=files,
)
print(response)
```

### Managing subscriptions

```python
from notification_sdk.client import ApiClient
from notification_sdk.subscriptions import SubscriptionEngine

client = ApiClient()
engine = SubscriptionEngine(client=client)

subscription = {
    "endpoint": "https://example.com/push/xyz",
    "keys": {
        "auth": "abc",
        "p256dh": "def",
    },
}

create_response = engine.create_subscription(
    customer_id="123456789",
    customer_email="customer@example.com",
    subscription=subscription,
)

get_response = engine.get_subscription(endpoint=subscription["endpoint"])
remove_response = engine.remove_subscription(endpoint=subscription["endpoint"])
```

## Testing

Run integration tests with:

```bash
pytest -s -v --log-cli-level=INFO -m integration
```

The tests rely on the environment variables defined in the `.env` file and sample data under `tests/integration/test_data.json`.

## Troubleshooting

- Missing environment variables will raise `ValueError` when `ApiClient` is initialized.
- HTTP errors from the API raise `requests.HTTPError` via `response.raise_for_status()`.
- Ensure file upload tuples follow the `requests` multipart format when using `files`.

## Notes

- The SDK does not include an API schema validator; it forwards payloads to the configured backend.
- The `base_url` must include the correct API host and prefix for the routes used by the SDK.
