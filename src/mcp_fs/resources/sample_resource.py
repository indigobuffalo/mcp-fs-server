"""Placeholder for a sample resource."""

from easy_mcp.registration.resources import mcp_resource


@mcp_resource("users://{user_id}/profile")
def get_user_file(user_id: str) -> dict:
    """
    name: get_user_file
    description: >
        Retrieve user information file based on user ID.

    Arguments:
        user_id (str): The ID of the user to retrieve information for.

    Returns:
        dict: A dictionary containing user information.

    Example:
        >>> get_user_info("12345")
        {'name': 'John Doe', 'email': 'sample_email@yahoo.com', 'user_id': '12345'}
    """
    import random

    return {
        "name": "John Doe",
        "email": "sample_email@yahoo.com",
        "user_id": user_id,
        "age": random.randint(18, 65),
    }
