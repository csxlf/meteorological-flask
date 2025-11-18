import os
from datetime import timedelta


class Config:
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456aA&@localhost:3306/meteo'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 密钥配置（用于会话加密）
    SECRET_KEY = os.urandom(24)

    # 登录配置
    REMEMBER_COOKIE_DURATION = timedelta(hours=2)

    # 静态资源路径配置
    STATIC_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    TEMPLATE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

    # 地图服务配置
    MAP_SERVICE_URL = 'http://localhost:8080/styles/OSM%20OpenMapTiles/#4/35.66/103.67'

    # 地区列表配置
    REGIONS = [
        '四川', '成都', '自贡', '攀枝花', '泸州', '德阳', '绵阳', '广元',
        '遂宁', '内江', '乐山', '南充', '眉山', '宜宾', '广安', '达州',
        '雅安', '巴中', '资阳', '阿坝州', '甘孜州', '凉山州'
    ]

    # 默认地区（成都）
    DEFAULT_REGION = '成都'