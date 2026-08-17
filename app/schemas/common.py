from enum import Enum


class CanonicalState(str, Enum):
    """Architecture Sec.29 — canonical state values."""

    WORKING = "working"
    APPROVED = "approved"
    LOCKED = "locked"
    CANONICAL = "canonical"
    ARCHIVED = "archived"
