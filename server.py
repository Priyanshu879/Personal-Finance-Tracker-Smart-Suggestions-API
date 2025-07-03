from flask import Flask, request, jsonify
import json
from suggestions import generate_suggestions
from flask_cors import CORS
from models import db, MonthlyReport
from suggestions import analyze_expenses

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Enable CORS for all routes
CORS(app, resources={r"/api/*": {"origins": "*"}})

db.init_app(app)

@app.before_request
def create_tables():
    db.create_all()


@app.route('/api/suggestions', methods=['POST'])
def get_suggestions():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    suggestions = generate_suggestions(data)
    return jsonify({'suggestions': suggestions})


@app.route("/api/reports", methods=["GET"])
def get_reports():
    user_id = request.args.get("user_id", "default_user")

    reports = MonthlyReport.query.filter_by(user_id=user_id)\
        .order_by(MonthlyReport.month.desc()).limit(3).all()

    result = [
        {
            "month": r.month,
            "total_spent": r.total_spent,
            "top_category": r.top_category,
            "overbudget_categories": r.overbudget_categories.split(",")
        }
        for r in reports
    ]
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
