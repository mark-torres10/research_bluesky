import os

SERVICE_DID = os.environ.get("SERVICE_DID", None)
HOSTNAME = os.environ.get("HOSTNAME", None)

if HOSTNAME is None:
    raise RuntimeError('You should set "HOSTNAME" environment variable first.')

if SERVICE_DID is None:
    SERVICE_DID = f"did:web:{HOSTNAME}"

ATTENTION_URI = os.environ.get("ATTENTION_URI")
CHRONOLOGICAL_URI = os.environ.get("CHRONOLOGICAL_URI")
PENALTY_URI = os.environ.get("PENALTY_URI")
