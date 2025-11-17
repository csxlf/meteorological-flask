from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required
from app import db
from app.models.task import TaskInfo, JobConfig, TaskStatus, TaskLog
import uuid

task_bp = Blueprint('task', __name__)


@task_bp.route('/manage')
@login_required
def manage():
    # 加载所有任务和作业配置
    tasks = TaskInfo.query.all()
    jobs = JobConfig.query.all()
    status_list = TaskStatus.query.all()
    logs = TaskLog.query.order_by(TaskLog.log_tm.desc()).all()

    return render_template('task/manage.html',
                           tasks=tasks,
                           jobs=jobs,
                           status_list=status_list,
                           logs=logs)


# 任务信息CRUD
@task_bp.route('/task/add', methods=['POST'])
@login_required
def add_task():
    data = request.form
    task = TaskInfo(
        pk=str(uuid.uuid4())[:20],
        task_name=data['task_name'],
        task_desc=data['task_desc'],
        currentbatch_tm=data.get('currentbatch_tm')
    )
    db.session.add(task)
    db.session.commit()
    flash('任务添加成功')
    return redirect(url_for('task.manage'))


@task_bp.route('/task/delete/<pk>')
@login_required
def delete_task(pk):
    task = TaskInfo.query.get(pk)
    if task:
        db.session.delete(task)
        db.session.commit()
        flash('任务删除成功')
    return redirect(url_for('task.manage'))


# 作业配置CRUD
@task_bp.route('/job/add', methods=['POST'])
@login_required
def add_job():
    data = request.form
    job = JobConfig(
        pk=str(uuid.uuid4())[:20],
        job_cd=data['job_cd'],
        jobtype_ecd=int(data['jobtype_ecd']),
        job_name=data.get('job_name'),
        jobcontent_desc=data.get('jobcontent_desc'),
        fixparam_desc=data.get('fixparam_desc')
    )
    db.session.add(job)
    db.session.commit()
    flash('作业配置添加成功')
    return redirect(url_for('task.manage'))


@task_bp.route('/job/delete/<pk>')
@login_required
def delete_job(pk):
    job = JobConfig.query.get(pk)
    if job:
        db.session.delete(job)
        db.session.commit()
        flash('作业配置删除成功')
    return redirect(url_for('task.manage'))