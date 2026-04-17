from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import mongo
from services.data_processor import load_and_clean, get_summary_stats, detect_anomalies
from services.ml_engine import run_linear_regression, run_clustering, generate_trend
import os

insights_bp = Blueprint("insights", __name__)

def get_file_path(dataset_id):
    dataset = mongo.db.datasets.find_one({"dataset_id": dataset_id})
    if not dataset:
        return None, None
    return os.path.join("uploads", dataset["saved_as"]), dataset

@insights_bp.route("/summary/<dataset_id>", methods=["GET"])
@jwt_required()
def summary(dataset_id):
    path, dataset = get_file_path(dataset_id)
    if not path:
        return jsonify({"error": "Dataset not found"}), 404

    df = load_and_clean(path)
    stats = get_summary_stats(df)
    return jsonify({
        "columns": list(df.columns),
        "row_count": len(df),
        "stats": stats
    }), 200

@insights_bp.route("/anomalies/<dataset_id>", methods=["GET"])
@jwt_required()
def anomalies(dataset_id):
    column = request.args.get("column")
    path, _ = get_file_path(dataset_id)
    if not path:
        return jsonify({"error": "Dataset not found"}), 404

    df = load_and_clean(path)
    result = detect_anomalies(df, column)
    return jsonify({"anomalies": result, "count": len(result)}), 200

@insights_bp.route("/regression/<dataset_id>", methods=["POST"])
@jwt_required()
def regression(dataset_id):
    data = request.get_json()
    target = data.get("target")
    features = data.get("features", [])

    path, _ = get_file_path(dataset_id)
    if not path:
        return jsonify({"error": "Dataset not found"}), 404

    df = load_and_clean(path)
    result = run_linear_regression(df, target, features)
    return jsonify(result), 200

@insights_bp.route("/cluster/<dataset_id>", methods=["POST"])
@jwt_required()
def cluster(dataset_id):
    data = request.get_json()
    n = data.get("n_clusters", 3)

    path, _ = get_file_path(dataset_id)
    if not path:
        return jsonify({"error": "Dataset not found"}), 404

    df = load_and_clean(path)
    result = run_clustering(df, n)
    return jsonify(result), 200

@insights_bp.route("/trend/<dataset_id>", methods=["GET"])
@jwt_required()
def trend(dataset_id):
    column = request.args.get("column")
    path, _ = get_file_path(dataset_id)
    if not path:
        return jsonify({"error": "Dataset not found"}), 404

    df = load_and_clean(path)
    result = generate_trend(df, column)
    return jsonify(result), 200