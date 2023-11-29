import os

SERVICE_DID = os.environ.get("SERVICE_DID", None)
HOSTNAME = os.environ.get("HOSTNAME", None)

if HOSTNAME is None:
    raise RuntimeError('You should set "HOSTNAME" environment variable first.')

if SERVICE_DID is None:
    SERVICE_DID = f"did:web:{HOSTNAME}"

# can get these after publishing each feed from publish_feed.py
ATTENTION_URI = os.environ.get("ATTENTION_URI")
# CHRONOLOGICAL_URI = os.environ.get("CHRONOLOGICAL_URI")
CHRONOLOGICAL_URI = (
    "at://did:plc:w5mjarupsl6ihdrzwgnzdh4y/app.bsky.feed.generator/time-feed"
)
PENALTY_URI = os.environ.get("PENALTY_URI")
