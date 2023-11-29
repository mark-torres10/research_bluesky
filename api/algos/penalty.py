"""A custom algorithm that penalizes emotional and moral information."""
from typing import Optional

from api import config

uri = config.PENALTY_URI


def handler(cursor: Optional[str], limit: int) -> dict:
    """Return a list of posts sorted by the penalty algorithm."""
    pass
