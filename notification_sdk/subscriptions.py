from .client import ApiClient
from .utils import generate_payload, generate_params
from typing import Any


class SubscriptionEngine:
    """Handles all subscription-related API operations."""

    def __init__(self, client: ApiClient):
        """
        Initialize SubscriptionEngine.

        Args:
            client: Authenticated ApiClient instance.
        """
        self.client = client

    def create_subscription(
        self, customer_id: str, customer_email: str, subscription: Any
    ) -> dict:
        """
        Create a new push notification subscription.

        Hits POST /api/subscription/subscribe.

        Args:
            customer_id: Unique identifier for the customer.
            customer_email: Email address of the customer.
            subscription: Subscription object containing endpoint and keys.

        Returns:
            Parsed JSON response from the API.

        Raises:
            requests.HTTPError: If the API returns a non-2xx status code.
        """
        payload = generate_payload(
            customer_id=customer_id,
            customer_email=customer_email,
            subscription=subscription,
        )
        response = self.client.post("/subscription/subscribe", payload)
        response.raise_for_status()
        return response.json()

    def get_subscription(self, endpoint: str) -> dict:
        """
        Retrieve an existing subscription by customer_email.

        Hits GET /api/subscription.

        Args:
            endpoint: The push subscription endpoint URL to look up.

        Returns:
            Parsed JSON response containing the subscription data.

        Raises:
            requests.HTTPError: If the API returns a non-2xx status code.
        """

        params = generate_params(endpoint=endpoint)
        response = self.client.get("/subscription", params=params)
        response.raise_for_status()
        return response.json()

    def remove_subscription(self, endpoint: str) -> dict:
        """
        Remove an existing push notification subscription.

        Hits POST /api/subscription/unsubscribe.

        Args:
            endpoint: The push subscription endpoint URL to remove.

        Returns:
            Parsed JSON response confirming removal.

        Raises:
            requests.HTTPError: If the API returns a non-2xx status code.
        """
        payload = generate_payload(endpoint=endpoint)
        response = self.client.post("/subscription/unsubscribe", payload)
        response.raise_for_status()
        return response.json()
