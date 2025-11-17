from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app.config import Config

# 初始化扩展
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 绑定扩展
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # 注册蓝图
    from app.routes.auth import bp as auth_bp
    from app.routes.weather import bp as weather_bp
    from app.routes.task import bp as task_bp
    from app.routes.forecast import bp as forecast_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(weather_bp, url_prefix='/weather')
    app.register_blueprint(task_bp, url_prefix='/task')
    app.register_blueprint(forecast_bp, url_prefix='/forecast')

    # 首页路由
    @app.route('/')
    def index():
        return redirect('/weather/realtime')

    return app


from app.models import weather, task, forecast