import os

feed_to_init_data_map = {
    "chronological": {
        "record_name": "time-feed",  # limit of 15 chars for name
        "display_name": "Chronological Feed",
        "description": "A feed that contains all the posts in chronological order.",
    },
    "attention": {
        "record_name": "attention-feed",
        "display_name": "Attention Feed",
        "description": "A feed that contains all the posts in attention order.",
    },
    "penalty": {
        "record_name": "penalty-feed",
        "display_name": "Penalty Feed",
        "description": "A feed that contains all the posts in penalty order.",
    },
}

BLUESKY_HOSTNAME = "feed.bsky.dev"
SERVICE_DID = ""
