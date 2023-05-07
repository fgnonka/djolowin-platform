""" This module contains the functions for calling webhook events."""

from django.db import transaction


def call_event(func_obj, *func_args, **func_kwargs):
    """Call webhook event with given arguments.
    Ensures that the atomic transaction is used.
    """
    connection = transaction.get_connection()
    if connection.in_atomic_block:
        transaction.on_commit(lambda: func_obj(*func_args, **func_kwargs))
    else:
        func_obj(*func_args, **func_kwargs)
