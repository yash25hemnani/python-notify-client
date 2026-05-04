from .client import ApiClient
from .utils import generate_payload, generate_params
from typing import Any


class NotificationEngine:
    """Handles all notification-related API operations."""

    def __init__(self, client: ApiClient):
        """
        Initialize NotificationEngine.

        Args:
            client: Authenticated ApiClient instance.
        """
        self.client = client

    def upload_email_attachments(self, files: list) -> list:
        response = self.client.post(
            "/notification/notify/upload-attachments", files=files
        )
        response.raise_for_status()
        return response.json()["data"]["paths"]

    def send_email_notification(
        self,
        customer_id: str,
        customer_email: str,
        template_slug: str,
        data: Any = None,
        cc: list = None,
        bcc: list = None,
        reply_to: str = None,
        files: list = None,
        file_paths: list = None,
    ) -> dict:
        uploaded_paths = []

        if files:
            # uploaded_paths = [{"path": "...", "originalname": "..."}, ...]
            uploaded_paths = self.upload_email_attachments(files)

        payload = generate_payload(
            customer_id=customer_id,
            customer_email=customer_email,
            template_slug=template_slug,
            data=data,
            cc=cc,
            bcc=bcc,
            reply_to=reply_to,
            file_paths=(file_paths or []),
            uploaded_paths=(uploaded_paths or []),
        )

        response = self.client.post("/notification/notify/email", payload)
        response.raise_for_status()
        return response.json()

    def send_push_notification(
        self,
        customer_id: str,
        customer_email: str,
        template_slug: str,
        data: Any,
    ) -> dict:
        """
        Send a push notification to a customer.

        Hits POST /api/notification/notify/push.

        Args:
            customer_id: Unique identifier for the customer.
            customer_email: Email address of the customer.
            template_slug: Slug of the push notification template to use.
            data: Dynamic data to populate the template.

        Returns:
            Parsed JSON response from the API.

        Raises:
            requests.HTTPError: If the API returns a non-2xx status code.
        """
        payload = generate_payload(
            customer_id=customer_id,
            customer_email=customer_email,
            template_slug=template_slug,
            data=data,
        )

        response = self.client.post("/notification/notify/push", payload)
        response.raise_for_status()
        return response.json()
