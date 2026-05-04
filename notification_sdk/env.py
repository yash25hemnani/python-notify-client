from dotenv import load_dotenv
import os

load_dotenv()


def get_env_variable(env_name: str, required: bool = True):
    value = os.getenv(env_name)

    if required and not value:
        raise ValueError(f"Missing required environment variable: {env_name}")

    return value


ENV = {
    "API_KEY": get_env_variable("API_KEY"),
    "BASE_URL": get_env_variable("BASE_URL"),
    "TEST_CUSTOMER_ID": get_env_variable("TEST_CUSTOMER_ID"),
    "TEST_CUSTOMER_EMAIL": get_env_variable("TEST_CUSTOMER_EMAIL"),
}
