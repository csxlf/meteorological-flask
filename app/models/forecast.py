from app import db
from datetime import date


class ForecastModel(db.Model):
    __tablename__ = 'METEO_FORECAST_MODEL'

    pk = db.Column(db.String(32), primary_key=True)
    model_ecd = db.Column(db.String(32), unique=True, nullable=False)
    model_no = db.Column(db.Integer, unique=True, nullable=True)
    model_name = db.Column(db.String(32), nullable=True)
    wth_beon_use_ecd = db.Column(db.Integer, nullable=True)
    atlst_run_tm = db.Column(db.Date, nullable=True)