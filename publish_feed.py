"""Publish feed."""
from atproto import Client, models

from constants import (
    HANDLE,
    PASSWORD,
    HOSTNAME,
    RECORD_NAME,
    DISPLAY_NAME,
    DESCRIPTION,
    SERVICE_DID,
)


def main():
    client = Client()
    client.login(HANDLE, PASSWORD)

    feed_did = SERVICE_DID

    avatar_blob = None

    response = client.com.atproto.repo.put_record(
        models.ComAtprotoRepoPutRecord.Data(
            repo=client.me.did,
            collection=models.ids.AppBskyFeedGenerator,
            rkey=RECORD_NAME,
            record=models.AppBskyFeedGenerator.Main(
                did=feed_did,
                display_name=DISPLAY_NAME,
                description=DESCRIPTION,
                avatar=avatar_blob,
                created_at=client.get_current_time_iso(),
            ),
        )
    )

    print("Successfully published!")
    print('Feed URI (put in "WHATS_ALF_URI" env var):', response.uri)


if __name__ == "__main__":
    main()
