from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.config import Config

# 初始化扩展（只创建对象，不绑定app）
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'task.login'  # 登录跳转路由
login_manager.login_message = '请先登录后再访问'


# 解决循环导入的关键：在回调函数内部导入User模型
@login_manager.user_loader
def load_user(user_id):
    # 延迟导入：只有在实际调用时才导入User，避免与models的循环依赖
    from app.models.task import User
    return User.query.get(int(user_id))


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 绑定扩展到app
    db.init_app(app)
    login_manager.init_app(app)

    # 注册蓝图（使用延迟导入，避免导入蓝图时触发模型导入）
    from app.routes.weather import weather_bp
    from app.routes.monitor import monitor_bp
    from app.routes.task import task_bp
    from app.routes.visforecast import visforecast_bp

    app.register_blueprint(weather_bp, url_prefix='/weather')
    app.register_blueprint(monitor_bp, url_prefix='/monitor')
    app.register_blueprint(task_bp, url_prefix='/task')
    app.register_blueprint(visforecast_bp, url_prefix='/visforecast')

    # 创建数据库表（在app上下文内执行）
    with app.app_context():
        db.create_all()

    return app