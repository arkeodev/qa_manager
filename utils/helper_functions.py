# utils/helper_functions.py

"""Helper functions for agent tasks."""

def is_termination_msg(message: dict) -> bool:
    """
    Check if a message is a termination message.

    Args:
        message (dict): The message to check.

    Returns:
        bool: True if it's a termination message, False otherwise.
    """
    return message.get('content', '').strip().upper() == 'TERMINATE'
