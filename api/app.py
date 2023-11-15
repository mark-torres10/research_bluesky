"""Flask app for API."""
from flask import Flask, jsonify
from flask_cors import CORS

from algos.attention import handler as attention_algo
from algos.chronological import handler as chronological_algo
from algos.penalty import handler as penalty_algo

app = Flask(__name__)
CORS(app)


map_type_to_algo = {
    "attention": attention_algo,
    "chronological": chronological_algo,
    "penalty": penalty_algo,
}


@app.route("/api/<algo_type>", methods=["POST"])
def reorder_feed_by_algo(algo_type: str) -> list[str]:
    pass


if __name__ == "__main__":
    pass
