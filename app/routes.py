from flask import Blueprint, jsonify, render_template

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/health")
def health():
    return jsonify({
        "status": "online",
        "application": "AI Security Operations Assistant",
        "version": "1.0.0",
    })
