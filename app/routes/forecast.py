from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required
from app import db
from app.models.forecast import ForecastModel
import uuid
import pymysql

forecast_bp = Blueprint('forecast', __name__)


@forecast_bp.route('/model')
@login_required
def model_manage():
    models = ForecastModel.query.all()
    return render_template('forecast/model.html', models=models)


# 模型CRUD
@forecast_bp.route('/model/add', methods=['POST'])
@login_required
def add_model():
    data = request.form
    model = ForecastModel(
        pk=str(uuid.uuid4()),
        model_ecd=data['model_ecd'],
        model_no=int(data.get('model_no', 0)),
        model_name=data.get('model_name'),
        wth_beon_use_ecd=int(data.get('wth_beon_use_ecd', 0)),
        atlst_run_tm=data.get('atlst_run_tm')
    )
    db.session.add(model)
    db.session.commit()
    flash('模型添加成功')
    return redirect(url_for('forecast.model_manage'))


@forecast_bp.route('/model/delete/<pk>')
@login_required
def delete_model(pk):
    model = ForecastModel.query.get(pk)
    if model:
        db.session.delete(model)
        db.session.commit()
        flash('模型删除成功')
    return redirect(url_for('forecast.model_manage'))


# 模型任务同步
@forecast_bp.route('/model/sync')
@login_required
def sync_model():
    # 连接数据库执行存储过程
    conn = db.engine.raw_connection()
    try:
        cursor = conn.cursor()
        # 调用存储过程
        cursor.callproc('pro_syc_models', [0])
        # 获取输出参数
        cursor.execute('SELECT @_pro_syc_models_0')
        result = cursor.fetchone()[0]
        conn.commit()

        if result >= 1:
            return jsonify({'status': 'success', 'msg': f'已完成同步，本次同步模型数量为{result}'})
        elif result == 0:
            return jsonify({'status': 'info', 'msg': '没有需要同步的模型'})
        else:
            return jsonify({'status': 'error', 'msg': '同步失败'})
    finally:
        conn.close()