from app import db
from flask_login import UserMixin  # 仅保留UserMixin导入，移除user_loader
from datetime import datetime


class User(UserMixin, db.Model):
    """用户模型，用于登录验证和权限管理"""
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)  # 用户名唯一
    password = db.Column(db.String(255), nullable=False)  # 存储加密后的密码
    is_admin = db.Column(db.SmallInteger, default=0)  # 0:普通用户 1:管理员，对应数据库TINYINT(1)

    def __repr__(self):
        return f'<User {self.username}>'


class TsTaskInfo(db.Model):
    """任务基本信息表"""
    __tablename__ = 'TS_TASKINFO'

    PK = db.Column(db.String(20), primary_key=True)  # 任务唯一标识
    TASK_NAME = db.Column(db.String(80), nullable=False)  # 任务名称
    TASK_DESC = db.Column(db.String(1000), nullable=False)  # 任务描述
    CurrentBatch_TM = db.Column(db.DateTime)  # 当前批次时间

    # 关联任务状态表（一对多）
    task_status = db.relationship(
        'TsTaskStatus',
        backref='task_info',  # 在TsTaskStatus中通过task_info访问当前任务
        lazy='dynamic',
        cascade='all, delete-orphan'  # 删除任务时级联删除关联的状态记录
    )

    def __repr__(self):
        return f'<TsTaskInfo {self.TASK_NAME}>'


class TsJobConfig(db.Model):
    """作业参数配置表"""
    __tablename__ = 'TS_JOBCONFIG'

    PK = db.Column(db.String(20), primary_key=True)  # 作业配置唯一标识
    JOB_CD = db.Column(db.String(20), nullable=False)  # 作业编码
    JobType_ECD = db.Column(db.Integer, nullable=False)  # 作业类型：1-定时 2-手动
    JOB_NAME = db.Column(db.String(200))  # 作业名称
    JobContent_DESC = db.Column(db.String(1000))  # 作业内容描述
    FixParam_DESC = db.Column(db.String(500))  # 固定参数描述

    # 关联任务状态表（一对多）
    task_status = db.relationship(
        'TsTaskStatus',
        backref='job_config',  # 在TsTaskStatus中通过job_config访问当前作业配置
        lazy='dynamic'
    )

    def __repr__(self):
        return f'<TsJobConfig {self.JOB_NAME}>'


class TsTaskStatus(db.Model):
    """任务运行状态表"""
    __tablename__ = 'TS_TaskStatus'

    PK = db.Column(db.String(20), primary_key=True)  # 状态记录唯一标识
    TS_TASKINFO_PK = db.Column(
        db.String(20),
        db.ForeignKey('TS_TASKINFO.PK'),
        nullable=False  # 关联任务ID（外键）
    )
    TS_JOBCONFIG_PK = db.Column(
        db.String(20),
        db.ForeignKey('TS_JOBCONFIG.PK'),
        nullable=False  # 关联作业配置ID（外键）
    )
    BATCH_TM = db.Column(db.DateTime)  # 批次时间
    STATUS_ECD = db.Column(db.Integer)  # 状态：1-运行中 2-已完成 3-失败
    START_TM = db.Column(db.DateTime)  # 开始时间
    END_TM = db.Column(db.DateTime)  # 结束时间
    ERRMSG_DESC = db.Column(db.String(4000))  # 错误信息（状态为失败时填写）

    def __repr__(self):
        return f'<TsTaskStatus {self.PK} - Status {self.STATUS_ECD}>'


class TsLog(db.Model):
    """作业日志表"""
    __tablename__ = 'TS_LOG'

    PK = db.Column(db.String(20), primary_key=True)  # 日志唯一标识
    LOG_TM = db.Column(db.DateTime, nullable=False)  # 日志时间
    EVENT_CD = db.Column(db.String(20))  # 事件编码
    MSG_DESC = db.Column(db.String(4000))  # 日志信息

    def __repr__(self):
        return f'<TsLog {self.LOG_TM}>'