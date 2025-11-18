from flask import Blueprint, render_template, request, jsonify
from app.models.weather import ObsData, StaInfo
from app import db
from datetime import datetime
import json

monitor_bp = Blueprint('monitor', __name__)


@monitor_bp.route('/')
def monitor_index():
    # 加载地区边界JSON
    with open('app/static/json/china_regions.json', 'r', encoding='utf-8') as f:
        regions_json = json.load(f)

    return render_template('monitor/index.html', regions_json=json.dumps(regions_json))


@monitor_bp.route('/get_monitor_data')
def get_monitor_data():
    """获取监测数据（根据阈值过滤）"""
    # 获取阈值参数
    temp_max = request.args.get('temp_max', type=float)
    temp_min = request.args.get('temp_min', type=float)
    rain_min = request.args.get('rain_min', type=float)
    vis_max = request.args.get('vis_max', type=float)
    wspeed_min = request.args.get('wspeed_min', type=float)

    # 查询最新数据（当前小时）
    current_time = datetime.now().strftime('%Y-%m-%d %H:00:00')
    obs_datas = ObsData.query.filter_by(obs_hour=current_time).all()

    # 按阈值过滤数据
    result = {
        'temp': [], 'rain': [], 'vis': [], 'wspeed': []
    }

    for data in obs_datas:
        # 气温过滤（介于min和max之间）
        if temp_min is not None and temp_max is not None and data.temp:
            if temp_min <= float(data.temp) <= temp_max:
                result['temp'].append({
                    'sta': data.sta,
                    'staname': data.sta_info.staname,
                    'lon': float(data.sta_info.lon),
                    'lat': float(data.sta_info.lat),
                    'value': float(data.temp)
                })

        # 降雨过滤（大于最小值）
        if rain_min is not None and data.rain:
            if float(data.rain) >= rain_min:
                result['rain'].append({
                    'sta': data.sta,
                    'staname': data.sta_info.staname,
                    'lon': float(data.sta_info.lon),
                    'lat': float(data.sta_info.lat),
                    'value': float(data.rain)
                })

        # 能见度过滤（小于最大值）
        if vis_max is not None and data.vis:
            if float(data.vis) <= vis_max:
                result['vis'].append({
                    'sta': data.sta,
                    'staname': data.sta_info.staname,
                    'lon': float(data.sta_info.lon),
                    'lat': float(data.sta_info.lat),
                    'value': float(data.vis)
                })

        # 风速过滤（大于最小值）
        if wspeed_min is not None and data.wspeed:
            if float(data.wspeed) >= wspeed_min:
                result['wspeed'].append({
                    'sta': data.sta,
                    'staname': data.sta_info.staname,
                    'lon': float(data.sta_info.lon),
                    'lat': float(data.sta_info.lat),
                    'value': float(data.wspeed)
                })

    return jsonify(result)