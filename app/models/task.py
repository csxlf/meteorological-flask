from app import db
from datetime import datetime


class TaskInfo(db.Model):
    __tablename__ = 'TS_TASKINFO'

    pk = db.Column(db.String(20), primary_key=True)
    task_name = db.Column(db.String(80), nullable=False)
    task_desc = db.Column(db.String(1000), nullable=False)
    currentbatch_tm = db.Column(db.DateTime, nullable=True)


class JobConfig(db.Model):
    __tablename__ = 'TS_JOBCONFIG'

    pk = db.Column(db.String(20), primary_key=True)
    job_cd = db.Column(db.String(20), nullable=False)
    jobtype_ecd = db.Column(db.Integer, nullable=False)
    job_name = db.Column(db.String(200), nullable=True)
    jobcontent_desc = db.Column(db.String(1000), nullable=True)
    fixparam_desc = db.Column(db.String(500), nullable=True)


class TaskStatus(db.Model):
    __tablename__ = 'TS_TaskStatus'

    pk = db.Column(db.String(20), primary_key=True)
    ts_taskinfo_pk = db.Column(db.String(20), db.ForeignKey('TS_TASKINFO.pk'), nullable=False)
    ts_jobconfig_pk = db.Column(db.String(20), db.ForeignKey('TS_JOBCONFIG.pk'), nullable=False)
    batch_tm = db.Column(db.DateTime, nullable=True)
    status_ecd = db.Column(db.Integer, nullable=True)
    start_tm = db.Column(db.DateTime, nullable=True)
    end_tm = db.Column(db.DateTime, nullable=True)
    errmsg_desc = db.Column(db.String(4000), nullable=True)


class TaskLog(db.Model):
    __tablename__ = 'TS_LOG'

    pk = db.Column(db.String(20), primary_key=True)
    log_tm = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    event_cd = db.Column(db.String(20), nullable=True)
    msg_desc = db.Column(db.String(4000), nullable=True)