from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from extensions import mongo
import pandas as pd
import os, uuid, datetime

upload_bp = Blueprint("upload", __name__)
ALLOWED_EXTENSIONS = {"csv", "xlsx", "xls"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route("/file", methods=["POST"])
@jwt_required()
def upload_file():
    user_id = get_jwt_identity()

    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if not allowed_file(file.filename):
        return jsonify({"error": "Only CSV and Excel files allowed"}), 400

    filename = secure_filename(file.filename)
    unique_name = f"{uuid.uuid4()}_{filename}"
    save_path = os.path.join("uploads", unique_name)
    file.save(save_path)

    # Read and store metadata
    try:
        df = pd.read_csv(save_path) if filename.endswith(".csv") else pd.read_excel(save_path)
        columns = list(df.columns)
        row_count = len(df)
    except Exception as e:
        return jsonify({"error": f"Could not parse file: {str(e)}"}), 400

    dataset_id = str(uuid.uuid4())
    mongo.db.datasets.insert_one({
        "dataset_id": dataset_id,
        "user_id": user_id,
        "filename": filename,
        "saved_as": unique_name,
        "columns": columns,
        "row_count": row_count,
        "uploaded_at": datetime.datetime.utcnow()
    })

    return jsonify({
        "message": "File uploaded successfully",
        "dataset_id": dataset_id,
        "columns": columns,
        "row_count": row_count
    }), 201

@upload_bp.route("/datasets", methods=["GET"])
@jwt_required()
def get_datasets():
    user_id = get_jwt_identity()
    datasets = list(mongo.db.datasets.find(
        {"user_id": user_id},
        {"_id": 0, "saved_as": 0}
    ))
    return jsonify({"datasets": datasets}), 200