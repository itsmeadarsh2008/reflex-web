"""Search bar component for the navbar."""

import reflex as rx
from .inkeep import inkeep


def search_bar() -> rx.Component:
    return rx.fragment(inkeep(width="100%"))
