from flask import Blueprint, render_template, request, jsonify, flash
from flask_login import login_required
from app.models.visforecast import MeteoForecastModel
from app import db
import uuid
from datetime import date
from sqlalchemy import text

visforecast_bp = Blueprint('visforecast', __name__)


@visforecast_bp.route('/')
@login_required
def index():
    models = MeteoForecastModel.query.all()
    return render_template('visforecast/index.html', models=models)


# 模型CRUD
@visforecast_bp.route('/model/add', methods=['POST'])
@login_required
def add_model():
    data = request.json
    # 检查编码唯一性
    if MeteoForecastModel.query.filter_by(model_ECD=data['model_ecd']).first():
        return jsonify({'success': False, 'msg': '模型编码已存在'})
    if data['model_no'] and MeteoForecastModel.query.filter_by(model_NO=data['model_no']).first():
        return jsonify({'success': False, 'msg': '模型版本号已存在'})

    model_id = str(uuid.uuid4())[:32]
    new_model = MeteoForecastModel(
        PK=model_id,
        model_ECD=data['model_ecd'],
        model_NO=data['model_no'],
        model_NAME=data['model_name'],
        WTH_BEON_USE_ECD=data['wth_beon_use_ecd'],
        ATLST_RUN_TM=date.fromisoformat(data['atlst_run_tm']) if data['atlst_run_tm'] else None
    )
    db.session.add(new_model)
    db.session.commit()
    return jsonify({'success': True, 'model_id': model_id})


@visforecast_bp.route('/model/edit', methods=['POST'])
@login_required
def edit_model():
    data = request.json
    model = MeteoForecastModel.query.get(data['pk'])
    if not model:
        return jsonify({'success': False, 'msg': '模型不存在'})

    # 检查编码唯一性（排除自身）
    if model.model_ECD != data['model_ecd'] and MeteoForecastModel.query.filter_by(model_ECD=data['model_ecd']).first():
        return jsonify({'success': False, 'msg': '模型编码已存在'})
    if data['model_no'] and model.model_NO != data['model_no'] and MeteoForecastModel.query.filter_by(
            model_NO=data['model_no']).first():
        return jsonify({'success': False, 'msg': '模型版本号已存在'})

    model.model_ECD = data['model_ecd']
    model.model_NO = data['model_no']
    model.model_NAME = data['model_name']
    model.WTH_BEON_USE_ECD = data['wth_beon_use_ecd']
    model.ATLST_RUN_TM = date.fromisoformat(data['atlst_run_tm']) if data['atlst_run_tm'] else None
    db.session.commit()
    return jsonify({'success': True})


@visforecast_bp.route('/model/delete/<pk>', methods=['POST'])
@login_required
def delete_model(pk):
    model = MeteoForecastModel.query.get(pk)
    if not model:
        return jsonify({'success': False, 'msg': '模型不存在'})
    db.session.delete(model)
    db.session.commit()
    return jsonify({'success': True})


@visforecast_bp.route('/model/sync', methods=['POST'])
@login_required
def sync_model():
    """模型任务同步"""
    try:
        # 调用存储过程
        result = db.session.execute(text("CALL pro_syc_models(@v_model_cnt)"))
        db.session.commit()
        # 获取输出参数
        v_model_cnt = db.session.execute(text("SELECT @v_model_cnt")).scalar()

        if v_model_cnt >= 1:
            return jsonify({'success': True, 'msg': f'已完成同步，本次同步模型数量为{v_model_cnt}'})
        elif v_model_cnt == 0:
            return jsonify({'success': True, 'msg': '没有需要同步的模型'})
        else:
            return jsonify({'success': False, 'msg': '同步失败'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'msg': f'同步异常：{str(e)}'})