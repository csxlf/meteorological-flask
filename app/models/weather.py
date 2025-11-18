from app import db
from datetime import datetime


class StaInfo(db.Model):
    __tablename__ = 'sta_info'
    sta = db.Column(db.String(10), primary_key=True)
    staname = db.Column(db.String(45))
    lon = db.Column(db.Numeric(16, 13))
    lat = db.Column(db.Numeric(16, 13))
    ati = db.Column(db.Numeric(6, 2))
    areacode = db.Column(db.String(6))

    # 关联观测数据
    obs_datas = db.relationship('ObsData', backref='sta_info', lazy='dynamic')


class ObsData(db.Model):
    __tablename__ = 'obs_data'
    sta = db.Column(db.String(10), db.ForeignKey('sta_info.sta'), primary_key=True)
    obs_hour = db.Column(db.DateTime, primary_key=True)
    temp = db.Column(db.Numeric(6, 2))
    rain = db.Column(db.Numeric(6, 2))
    press = db.Column(db.Numeric(6, 2))
    vis = db.Column(db.Numeric(7, 2))
    wspeed = db.Column(db.Numeric(6, 2))
    wdirection = db.Column(db.Integer)
    rh = db.Column(db.Integer)
    dewpoint = db.Column(db.Numeric(6, 2))
    totalcloud = db.Column(db.Integer)
    lowcloud = db.Column(db.Integer)
    lowcloudamount = db.Column(db.Integer)
    lowcloudheight = db.Column(db.Integer)


class Area(db.Model):
    __tablename__ = 'area'
    areacode = db.Column(db.String(6), primary_key=True)
    areaname = db.Column(db.String(50))
    type = db.Column(db.String(10))