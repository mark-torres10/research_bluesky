"""Flask app for API.

Based on https://github.com/MarshalX/bluesky-feed-generator/blob/main/server/app.py
"""  # noqa
import sys
import signal
import threading

from flask import Flask, jsonify, request
from flask_cors import CORS

from algos.attention import handler as attention_algo
from algos.chronological import handler as chronological_algo
from algos.penalty import handler as penalty_algo
from api import config
from api import data_stream
from api.data_filter import operations_callback
from api.algos import algos

app = Flask(__name__)
CORS(app)


map_type_to_algo = {
    "attention": attention_algo,
    "chronological": chronological_algo,
    "penalty": penalty_algo,
}

stream_stop_event = threading.Event()
stream_thread = threading.Thread(
    target=data_stream.run,
    args=(
        config.SERVICE_DID,
        operations_callback,
        stream_stop_event,
    ),
)
stream_thread.start()


def sigint_handler(*_):
    print("Stopping data stream...")
    stream_stop_event.set()
    sys.exit(0)


signal.signal(signal.SIGINT, sigint_handler)


@app.route("/")
def index():
    return "AT Protocol Feed Generator"


@app.route("/.well-known/did.json", methods=["GET"])
def did_json():
    if not config.SERVICE_DID.endswith(config.HOSTNAME):
        return "", 404

    return jsonify(
        {
            "@context": ["https://www.w3.org/ns/did/v1"],
            "id": config.SERVICE_DID,
            "service": [
                {
                    "id": "#bsky_fg",
                    "type": "BskyFeedGenerator",
                    "serviceEndpoint": f"https://{config.HOSTNAME}",
                }
            ],
        }
    )


@app.route("/xrpc/app.bsky.feed.describeFeedGenerator", methods=["GET"])
def describe_feed_generator():
    feeds = [{"uri": uri} for uri in algos.keys()]
    response = {
        "encoding": "application/json",
        "body": {"did": config.SERVICE_DID, "feeds": feeds},
    }
    return jsonify(response)


@app.route("/xrpc/app.bsky.feed.getFeedSkeleton", methods=["GET"])
def get_feed_skeleton():
    feed = request.args.get("feed", default=None, type=str)
    algo = algos.get(feed)
    if not algo:
        return "Unsupported algorithm", 400

    try:
        cursor = request.args.get("cursor", default=None, type=str)
        limit = request.args.get("limit", default=20, type=int)
        body = algo(cursor, limit)
    except ValueError:
        return "Malformed cursor", 400

    return jsonify(body)


if __name__ == "__main__":
    pass
