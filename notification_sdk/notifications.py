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
            # uploaded_paths = [{"id": "...", "path": "...", "originalname": "..."}, ...]
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

    def get_push_notifications(
        self,
        customer_email: str,
        page: int = 1,
        limit: int = 10,
    ) -> dict:
        """
        Retrieve paginated push notifications for a customer.

        Hits GET /api/notification/notify/push/all.

        Args:
            customer_email: Email address of the customer.
            page: Page number for pagination (default: 1).
            limit: Number of notifications per page (default: 10).

        Returns:
            Parsed JSON response from the API with paginated notifications.

        Raises:
            requests.HTTPError: If the API returns a non-2xx status code.
        """
        params = generate_params(
            customerEmail=customer_email,
            page=page,
            limit=limit,
        )

        response = self.client.get("/notification/notify/push/all", params=params)
        response.raise_for_status()
        return response.json()

    def mark_as_read(
        self,
        customer_email: str,
        notification_id: str,
    ) -> dict:
        """
        Mark a specific push notification as read.

        Hits PATCH /api/notification/notify/push/mark-as-read.

        Args:
            customer_email: Email address of the customer.
            notification_id: Unique identifier of the notification to mark as read.

        Returns:
            Parsed JSON response from the API.

        Raises:
            requests.HTTPError: If the API returns a non-2xx status code.
        """
        payload = generate_payload(
            customerEmail=customer_email,
            notificationId=notification_id,
        )

        response = self.client.patch("/notification/notify/push/mark-as-read", payload)
        response.raise_for_status()
        return response.json()

    def mark_all_as_read(
        self,
        customer_email: str,
    ) -> dict:
        """
        Mark all push notifications as read for a customer.

        Hits PATCH /api/notification/notify/push/mark-all-as-read.

        Args:
            customer_email: Email address of the customer.

        Returns:
            Parsed JSON response from the API.

        Raises:
            requests.HTTPError: If the API returns a non-2xx status code.
        """
        payload = generate_payload(
            customerEmail=customer_email,
        )

        response = self.client.patch("/notification/notify/push/mark-all-as-read", payload)
        response.raise_for_status()
        return response.json()