from app import db
from datetime import date

class MeteoForecastModel(db.Model):
    __tablename__ = 'METEO_FORECAST_MODEL'
    PK = db.Column(db.String(32), primary_key=True)
    model_ECD = db.Column(db.String(32), unique=True, nullable=False)
    model_NO = db.Column(db.Integer, unique=True)
    model_NAME = db.Column(db.String(32))
    WTH_BEON_USE_ECD = db.Column(db.Integer)
    ATLST_RUN_TM = db.Column(db.Date)