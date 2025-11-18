from flask import Blueprint, render_template, request, jsonify
from app.models.weather import StaInfo, ObsData, Area
from app import db
from datetime import datetime, timedelta
import json

weather_bp = Blueprint('weather', __name__)


@weather_bp.route('/query')
def weather_query():
    # 获取默认地区和当前时间
    default_region = request.args.get('region', '成都')
    current_time = datetime.now().strftime('%Y-%m-%d %H:00:00')

    # 加载地区边界JSON
    with open('app/static/json/sc.json', 'r', encoding='utf-8') as f:
        regions_json = json.load(f)
    print("边界数据是否加载成功：", len(regions_json.get('features', [])) > 0)

    return render_template('weather/query.html',
                           default_region=default_region,
                           current_time=current_time,
                           regions_json=json.dumps(regions_json))


@weather_bp.route('/get_stations')
def get_stations():
    """获取站点数据"""
    region = request.args.get('region', '成都')
    # 根据地区获取站点（实际需关联area表，此处简化）
    stations = StaInfo.query.all()
    result = [{
        'sta': s.sta,
        'staname': s.staname,
        'lon': float(s.lon),
        'lat': float(s.lat)
    } for s in stations]
    return jsonify(result)


@weather_bp.route('/get_obs_data')
def get_obs_data():
    """获取观测数据"""
    obs_time = request.args.get('time')
    elements = request.args.getlist('elements[]')

    if not obs_time:
        return jsonify({'error': '时间参数必填'}), 400

    # 转换时间格式
    try:
        obs_time = datetime.strptime(obs_time, '%Y-%m-%d %H:00:00')
    except ValueError:
        return jsonify({'error': '时间格式错误'}), 400

    # 查询数据
    obs_datas = ObsData.query.filter_by(obs_hour=obs_time).all()
    result = []
    for data in obs_datas:
        item = {'sta': data.sta, 'staname': data.sta_info.staname}
        # 根据选择的要素返回对应数据
        if 'temp' in elements:
            item['temp'] = float(data.temp) if data.temp else None
        if 'rain' in elements:
            item['rain'] = float(data.rain) if data.rain else None
        if 'rh' in elements:
            item['rh'] = data.rh if data.rh else None
        if 'press' in elements:
            item['press'] = float(data.press) if data.press else None
        if 'wspeed' in elements or 'wdirection' in elements:
            item['wspeed'] = float(data.wspeed) if data.wspeed else None
            item['wdirection'] = data.wdirection if data.wdirection else None
        if 'vis' in elements:
            item['vis'] = float(data.vis) if data.vis else None
        result.append(item)

    return jsonify(result)


@weather_bp.route('/get_table_data')
def get_table_data():
    """获取表格数据"""
    obs_time = request.args.get('time')
    if not obs_time:
        return jsonify({'error': '时间参数必填'}), 400

    try:
        obs_time = datetime.strptime(obs_time, '%Y-%m-%d %H:00:00')
    except ValueError:
        return jsonify({'error': '时间格式错误'}), 400

    # 查询数据并关联站点信息
    data = db.session.query(ObsData, StaInfo).join(StaInfo, ObsData.sta == StaInfo.sta) \
        .filter(ObsData.obs_hour == obs_time).all()

    result = []
    for obs, sta in data:
        result.append({
            'sta': obs.sta,
            'staname': sta.staname,
            'temp': float(obs.temp) if obs.temp else '-',
            'rain': float(obs.rain) if obs.rain else '-',
            'press': float(obs.press) if obs.press else '-',
            'vis': float(obs.vis) if obs.vis else '-',
            'wspeed': float(obs.wspeed) if obs.wspeed else '-',
            'wdirection': obs.wdirection if obs.wdirection else '-',
            'rh': obs.rh if obs.rh else '-',
            'dewpoint': float(obs.dewpoint) if obs.dewpoint else '-'
        })

    return jsonify(result)