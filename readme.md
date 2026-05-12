# Python Notification SDK

A lightweight SDK for sending email and push notifications, uploading email attachments, and managing push notification subscriptions through a REST API.

## Features

- Send email notifications with optional attachments and recipient overrides
- Send push notifications with template-based dynamic content
- Create, retrieve, and remove push notification subscriptions
- Automatically convert Python `snake_case` payload keys to API-friendly `camelCase`
- Simple configuration via environment variables or `.env` file

## Installation

```bash
python -m pip install -r requirements.txt
```

To install the package locally:

```bash
python -m pip install .
```

## Configuration

Create a `.env` file in the project root or set the following environment variables:

```bash
API_KEY=your_api_key
BASE_URL=https://api.example.com
TEST_CUSTOMER_ID=123456789
TEST_CUSTOMER_EMAIL=test@example.com
```

The package uses `python-dotenv` to load environment variables from `.env` when available.

## Package Structure

- `notification_sdk/client.py` — HTTP client for authenticated API requests
- `notification_sdk/env.py` — environment variable loader and required configuration
- `notification_sdk/notifications.py` — email and push notification operations
- `notification_sdk/subscriptions.py` — subscription management operations
- `notification_sdk/utils.py` — payload and parameter helpers

## Usage Examples

### Initialize the client

```python
from notification_sdk.client import ApiClient
from notification_sdk.notifications import NotificationEngine
from notification_sdk.subscriptions import SubscriptionEngine

client = ApiClient()
notification_engine = NotificationEngine(client=client)
subscription_engine = SubscriptionEngine(client=client)
```

### Send a push notification

```python
response = notification_engine.send_push_notification(
    customer_id="123456789",
    customer_email="customer@example.com",
    template_slug="welcome-new-user",
    data={"name": "Jane"},
)
print(response)
```

### Send an email notification

```python
files = [
    (
        "files",
        ("invoice.pdf", open("invoice.pdf", "rb"), "application/pdf"),
    ),
]

response = notification_engine.send_email_notification(
    customer_id="123456789",
    customer_email="customer@example.com",
    template_slug="order-confirmation",
    data={"name": "Jane"},
    cc=["manager@example.com"],
    bcc=["audit@example.com"],
    reply_to="support@example.com",
    file_paths=["/attachments/invoice.pdf"],
    files=files,
)
print(response)
```

### Create a subscription

```python
subscription = {
    "endpoint": "https://example.com/fcm/send/abc123",
    "keys": {
        "auth": "auth-token",
        "p256dh": "p256dh-key",
    },
}

response = subscription_engine.create_subscription(
    customer_id="123456789",
    customer_email="customer@example.com",
    subscription=subscription,
)
print(response)
```

### Retrieve a subscription

```python
response = subscription_engine.get_subscription(
    endpoint="https://example.com/fcm/send/abc123"
)
print(response)
```

### Remove a subscription

```python
response = subscription_engine.remove_subscription(
    endpoint="https://example.com/fcm/send/abc123"
)
print(response)
```

## Running Tests

The repository includes integration tests under `tests/integration`.

```bash
pytest -s -v --log-cli-level=INFO -m integration
```

## Notes

- `ApiClient.post()` sends multipart form data when `files` are provided and JSON otherwise.
- `generate_payload()` strips `None` values and converts keys from `snake_case` to `camelCase`.
- API responses are expected to include `success` and `data` keys.
