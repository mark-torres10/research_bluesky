"""Create a new feed and publish the feed.

Example:
    $ python publish_feed.py chronological

    $ python publish_feed.py attention

    $ python publish_feed.py penalty
"""
from dotenv import load_dotenv
import os
import sys

from atproto import Client, models

from constants import feed_to_init_data_map, BLUESKY_HOSTNAME, SERVICE_DID

load_dotenv()
handle = os.getenv("BLUESKY_HANDLE")
password = os.getenv("BLUESKY_PASSWORD")


def main():
    feed_name = sys.argv[1]
    record_name = feed_to_init_data_map[feed_name]["record_name"]
    display_name = feed_to_init_data_map[feed_name]["display_name"]
    description = feed_to_init_data_map[feed_name]["description"]

    client = Client()
    client.login(handle, password)

    feed_did = SERVICE_DID
    if not feed_did:
        feed_did = f"did:web:{BLUESKY_HOSTNAME}"

    avatar_blob = None

    response = client.com.atproto.repo.put_record(
        models.ComAtprotoRepoPutRecord.Data(
            repo=client.me.did,
            collection=models.ids.AppBskyFeedGenerator,
            rkey=record_name,
            record=models.AppBskyFeedGenerator.Main(
                did=feed_did,
                display_name=display_name,
                description=description,
                avatar=avatar_blob,
                created_at=client.get_current_time_iso(),
            ),
        )
    )

    print("Successfully published!")
    print(f"Feed URI for '{feed_name}' feed:", response.uri)


if __name__ == "__main__":
    main()
