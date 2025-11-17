# app/config.py
import os
from datetime import timedelta
from dotenv import load_dotenv  # 新增：加载.env文件

# 加载.env环境变量
load_dotenv()


class Config:
    # 从.env读取密钥（不再硬编码）
    SECRET_KEY = os.getenv('SECRET_KEY') or 'fallback_hard_to_guess_string'

    # 从.env读取MySQL配置（避免密码泄露）
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DB')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 静态资源缓存控制
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=0)

    # 从.env读取地图服务地址
    MAP_SERVICE_URL = os.getenv('MAP_SERVICE_URL')