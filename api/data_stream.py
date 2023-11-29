from atproto import CAR, AtUri, models
from atproto.exceptions import FirehoseError
from atproto.firehose import FirehoseSubscribeReposClient
from atproto.xrpc_client.models.common import XrpcError

from api.database import SubscriptionState


def run(name, operations_callback, stream_stop_event=None):
    """Receive data from firehose and run operations callback on it until
    stream_stop_event is set (i.e., Ctrl + C)."""
    while stream_stop_event is None or not stream_stop_event.is_set():
        try:
            _run(name, operations_callback, stream_stop_event)
        except FirehoseError as e:
            if e.args:
                xrpc_error = e.args[0]
                if (
                    isinstance(xrpc_error, XrpcError)
                    and xrpc_error.error == "ConsumerTooSlow"
                ):
                    print("Reconnecting to Firehose due to ConsumerTooSlow...")
                    continue

            raise e


def _run(name, operations_callback, stream_stop_event=None):
    state = SubscriptionState.select(SubscriptionState.service == name).first()
    params = None
    if state:
        params = models.ComAtprotoSyncSubscribeRepos.Params(cursor=state.cursor)
    client = FirehoseSubscribeReposClient(params)
    if not state:
        SubscriptionState.create(service=name, cursor=0)

    def on_message_handler():
        pass

    client.start(on_message_handler)
