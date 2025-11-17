from app import db


class Area(db.Model):
    __tablename__ = 'area'
    areacode = db.Column(db.CHAR(6), primary_key=True, nullable=False)
    areaname = db.Column(db.VARCHAR(50))
    type = db.Column(db.VARCHAR(10))

    # 关联站点
    stations = db.relationship('StaInfo', backref='area', lazy='dynamic')


class StaInfo(db.Model):
    __tablename__ = 'sta_info'
    sta = db.Column(db.VARCHAR(10), primary_key=True, nullable=False)
    staname = db.Column(db.VARCHAR(45))
    lon = db.Column(db.DECIMAL(16, 13))
    lat = db.Column(db.DECIMAL(16, 13))
    ati = db.Column(db.DECIMAL(6, 2))
    areacode = db.Column(db.CHAR(6), db.ForeignKey('area.areacode'))

    # 关联实况数据
    obs_data = db.relationship('ObsData', backref='station', lazy='dynamic')


class ObsData(db.Model):
    __tablename__ = 'obs_data'
    sta = db.Column(db.VARCHAR(10), db.ForeignKey('sta_info.sta'), primary_key=True, nullable=False)
    obs_hour = db.Column(db.DATETIME, primary_key=True, nullable=False)
    temp = db.Column(db.DECIMAL(6, 2))
    rain = db.Column(db.DECIMAL(6, 2))
    press = db.Column(db.DECIMAL(6, 2))
    vis = db.Column(db.DECIMAL(7, 2))
    wspeed = db.Column(db.DECIMAL(6, 2))
    wdirection = db.Column(db.INTEGER)
    rh = db.Column(db.INTEGER)
    dewpoint = db.Column(db.DECIMAL(6, 2))
    totalcloud = db.Column(db.INTEGER)
    lowcloud = db.Column(db.INTEGER)
    lowcloudamount = db.Column(db.INTEGER)
    lowcloudheight = db.Column(db.INTEGER)