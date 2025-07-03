from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class MonthlyReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    month = db.Column(db.String(20), nullable=False)
    total_spent = db.Column(db.Float, nullable=False)
    top_category = db.Column(db.String(100))
    overbudget_categories = db.Column(db.Text)  # Comma-separated
