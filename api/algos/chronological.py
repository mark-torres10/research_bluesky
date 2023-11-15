"""Reverse chronological ordering of the posts in the feed."""
from typing import Optional

from algos.helper import CURSOR_EOF

from database import Post


def handler(cursor: Optional[str], limit: int) -> dict:
    posts = (
        Post.select()
        .order_by(Post.cid.desc())
        .order_by(Post.indexed_at.desc())
        .limit(limit)
    )

    if cursor:
        if cursor == CURSOR_EOF:
            return {"cursor": CURSOR_EOF, "feed": []}
        cursor_parts = cursor.split("::")
        if len(cursor_parts) != 2:
            raise ValueError("Malformed cursor")

    feed = [{"post": post.uri} for post in posts]

    cursor = CURSOR_EOF
    last_post = posts[-1] if posts else None
    if last_post:
        cursor = (
            f"{int(last_post.indexed_at.timestamp() * 1000)}::{last_post.cid}"  # noqa
        )

    return {"cursor": cursor, "feed": feed}
