from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from app.models.task import User, TsTaskInfo, TsJobConfig, TsTaskStatus, TsLog
from app import db
from datetime import datetime
import uuid

task_bp = Blueprint('task', __name__)


@task_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect(url_for('task.index'))
        flash('用户名或密码错误')

    return render_template('task/login.html')


@task_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('task.login'))


@task_bp.route('/')
@login_required
def index():
    # 任务信息和作业配置
    tasks = TsTaskInfo.query.all()
    job_configs = TsJobConfig.query.all()
    return render_template('task/index.html', tasks=tasks, job_configs=job_configs)


@task_bp.route('/status')
@login_required
def status():
    # 任务状态和日志
    task_status = TsTaskStatus.query.all()
    logs = TsLog.query.order_by(TsLog.LOG_TM.desc()).all()
    return render_template('task/status.html', task_status=task_status, logs=logs)


# 任务信息CRUD
@task_bp.route('/task/add', methods=['POST'])
@login_required
def add_task():
    data = request.json
    task_id = str(uuid.uuid4()).replace('-', '')[:20]
    new_task = TsTaskInfo(
        PK=task_id,
        TASK_NAME=data['task_name'],
        TASK_DESC=data['task_desc'],
        CurrentBatch_TM=datetime.strptime(data['current_batch_tm'], '%Y-%m-%d %H:%M:%S') if data[
            'current_batch_tm'] else None
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'success': True, 'task_id': task_id})


@task_bp.route('/task/edit', methods=['POST'])
@login_required
def edit_task():
    data = request.json
    task = TsTaskInfo.query.get(data['pk'])
    if not task:
        return jsonify({'success': False, 'msg': '任务不存在'})
    task.TASK_NAME = data['task_name']
    task.TASK_DESC = data['task_desc']
    task.CurrentBatch_TM = datetime.strptime(data['current_batch_tm'], '%Y-%m-%d %H:%M:%S') if data[
        'current_batch_tm'] else None
    db.session.commit()
    return jsonify({'success': True})


@task_bp.route('/task/delete/<pk>', methods=['POST'])
@login_required
def delete_task(pk):
    task = TsTaskInfo.query.get(pk)
    if not task:
        return jsonify({'success': False, 'msg': '任务不存在'})
    db.session.delete(task)
    db.session.commit()
    return jsonify({'success': True})


# 作业配置CRUD（类似任务信息，省略重复逻辑）
@task_bp.route('/job/add', methods=['POST'])
@login_required
def add_job():
    data = request.json
    job_id = str(uuid.uuid4()).replace('-', '')[:20]
    new_job = TsJobConfig(
        PK=job_id,
        JOB_CD=data['job_cd'],
        JobType_ECD=data['job_type_ecd'],
        JOB_NAME=data['job_name'],
        JobContent_DESC=data['job_content_desc'],
        FixParam_DESC=data['fix_param_desc']
    )
    db.session.add(new_job)
    db.session.commit()
    return jsonify({'success': True, 'job_id': job_id})


@task_bp.route('/job/edit', methods=['POST'])
@login_required
def edit_job():
    data = request.json
    job = TsJobConfig.query.get(data['pk'])
    if not job:
        return jsonify({'success': False, 'msg': '作业配置不存在'})
    job.JOB_CD = data['job_cd']
    job.JobType_ECD = data['job_type_ecd']
    job.JOB_NAME = data['job_name']
    job.JobContent_DESC = data['job_content_desc']
    job.FixParam_DESC = data['fix_param_desc']
    db.session.commit()
    return jsonify({'success': True})


@task_bp.route('/job/delete/<pk>', methods=['POST'])
@login_required
def delete_job(pk):
    job = TsJobConfig.query.get(pk)
    if not job:
        return jsonify({'success': False, 'msg': '作业配置不存在'})
    db.session.delete(job)
    db.session.commit()
    return jsonify({'success': True})