from flask import Blueprint, make_response, request
from flask_jwt_extended import jwt_required
from fpdf import FPDF
from services.data_processor import load_and_clean, get_summary_stats
from extensions import mongo
import io, csv, os

export_bp = Blueprint("export", __name__)

def get_dataset_path(dataset_id):
    d = mongo.db.datasets.find_one({"dataset_id": dataset_id})
    return os.path.join("uploads", d["saved_as"]) if d else None

@export_bp.route("/csv/<dataset_id>", methods=["GET"])
@jwt_required()
def export_csv(dataset_id):
    path = get_dataset_path(dataset_id)
    if not path:
        return {"error": "Not found"}, 404

    df = load_and_clean(path)
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)

    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = f"attachment; filename=export_{dataset_id}.csv"
    response.headers["Content-Type"] = "text/csv"
    return response

@export_bp.route("/pdf/<dataset_id>", methods=["GET"])
@jwt_required()
def export_pdf(dataset_id):
    path = get_dataset_path(dataset_id)
    if not path:
        return {"error": "Not found"}, 404

    df = load_and_clean(path)
    stats = get_summary_stats(df)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 12, "AI Insights Report", ln=True)
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, f"Dataset: {dataset_id}", ln=True)
    pdf.cell(0, 8, f"Total rows: {len(df)}", ln=True)
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 10, "Column Summary Statistics", ln=True)
    pdf.set_font("Helvetica", "", 11)

    for col, s in stats.items():
        pdf.cell(0, 8, f"{col}: mean={s['mean']}, min={s['min']}, max={s['max']}", ln=True)

    response = make_response(bytes(pdf.output()))
    response.headers["Content-Disposition"] = f"attachment; filename=report_{dataset_id}.pdf"
    response.headers["Content-Type"] = "application/pdf"
    return response