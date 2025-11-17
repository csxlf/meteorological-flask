from flask_login import UserMixin
from app import db, login_manager
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'sys_user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)


# 登录管理器用户加载回调
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))