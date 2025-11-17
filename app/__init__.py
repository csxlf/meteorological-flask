# app/__init__.py
# 应用初始化核心文件：初始化扩展、注册蓝图、创建应用实例
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.config import Config  # 导入配置类

# ---------------------- 初始化扩展实例 ----------------------
# 数据库扩展（全局唯一，需在create_app外初始化，避免重复创建）
db = SQLAlchemy()
# 登录管理扩展（控制用户登录状态）
login_manager = LoginManager()
# 未登录用户访问需登录路由时，跳转至auth.login视图
login_manager.login_view = "auth.login"
# 登录页面提示信息类别（Bootstrap样式适配）
login_manager.login_message_category = "info"


# ---------------------- 创建Flask应用实例 ----------------------
def create_app(config_class: type = Config) -> Flask:
    """
    创建并配置Flask应用实例
    :param config_class: 配置类（默认使用Config，可扩展为开发/生产环境配置）
    :return: 配置完成的Flask应用实例
    """
    app = Flask(__name__)
    # 加载配置（从配置类读取数据库、密钥等配置）
    app.config.from_object(config_class)

    # ---------------------- 初始化扩展与应用关联 ----------------------
    db.init_app(app)  # 数据库扩展绑定应用
    login_manager.init_app(app)  # 登录管理扩展绑定应用

    # ---------------------- 注册路由蓝图（模块化拆分） ----------------------
    # 1. 认证蓝图（登录/退出，无URL前缀）
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    # 2. 气象实况查询蓝图（URL前缀：/weather）
    from app.routes.weather import weather_bp
    app.register_blueprint(weather_bp, url_prefix="/weather")

    # 3. 实况监测蓝图（URL前缀：/monitor，预留功能）
    from app.routes.monitor import monitor_bp
    app.register_blueprint(monitor_bp, url_prefix="/monitor")

    # 4. 后台任务管理蓝图（URL前缀：/task）
    from app.routes.task import task_bp
    app.register_blueprint(task_bp, url_prefix="/task")

    # 5. 能见度预报模型管理蓝图（URL前缀：/forecast）
    from app.routes.forecast import forecast_bp
    app.register_blueprint(forecast_bp, url_prefix="/forecast")

    # ---------------------- 初始化数据库表（首次运行自动创建） ----------------------
    with app.app_context():  # 激活应用上下文（确保db能找到应用配置）
        db.create_all()  # 创建所有模型对应的数据库表（若表已存在则不重复创建）

    return app


# ---------------------- 登录管理器回调（加载用户） ----------------------
@login_manager.user_loader
def load_user(user_id: str):
    """
    Flask-Login 要求的回调函数：根据用户ID加载用户实例
    :param user_id: 用户ID（字符串格式，从Session中获取）
    :return: 用户实例（User类对象）或None
    """
    from app.models.user import User  # 延迟导入，避免循环依赖
    return User.query.get(int(user_id))  # 通过ID查询用户