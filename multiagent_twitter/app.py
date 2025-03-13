from flask import Flask, render_template, request, jsonify
from bot import create_post
from logic.entities import TopicRequest

app = Flask(__name__)


@app.route("/")
def index():
    """Render the main HTML page."""
    return render_template("index.html")


@app.route("/create_post", methods=["POST"])
def create_post_endpoint():
    """Endpoint API to create a post based on a provided topic."""
    topic = request.json.get("topic")
    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    try:
        create_post(topic)
        return jsonify({"message": "Tweet generated and processed successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
