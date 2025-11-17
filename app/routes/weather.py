from flask import Blueprint, render_template, jsonify, request
from app import db
from app.models.weather import Area, StaInfo, ObsData
from datetime import datetime, timedelta
import json

bp = Blueprint('weather', __name__)

# 加载地区边界JSON（本地文件）
with open('app/static/json/area_boundaries.json', 'r', encoding='utf-8') as f:
    AREA_BOUNDARIES = json.load(f)


@bp.route('/realtime')
def realtime():
    # 默认地区：成都（areacode=510100）
    default_area = Area.query.filter_by(areaname='成都').first()
    # 所有地区列表
    areas = Area.query.filter(Area.areaname.in_(
        ['四川', '成都', '自贡', '攀枝花', '泸州', '德阳', '绵阳', '广元', '遂宁', '内江',
         '乐山', '南充', '眉山', '宜宾', '广安', '达州', '雅安', '巴中', '资阳', '阿坝州',
         '甘孜州', '凉山州']
    )).all()
    # 默认时间：当前时间
    current_time = datetime.now().strftime('%Y-%m-%d %H:00:00')
    return render_template('weather/realtime.html',
                           default_area=default_area,
                           areas=areas,
                           current_time=current_time,
                           map_service_url=current_app.config['MAP_SERVICE_URL'])


@bp.route('/api/get_obs_data')
def get_obs_data():
    # 获取请求参数
    area_code = request.args.get('area_code')
    obs_time = datetime.strptime(request.args.get('obs_time'), '%Y-%m-%d %H:00:00')
    elements = request.args.getlist('elements[]')

    # 查询该地区所有站点
    stations = StaInfo.query.filter_by(areacode=area_code).all()
    sta_codes = [s.sta for s in stations]

    # 查询对应时间的实况数据
    obs_data = ObsData.query.filter(
        ObsData.sta.in_(sta_codes),
        ObsData.obs_hour == obs_time
    ).all()

    # 格式化返回数据
    result = []
    for data in obs_data:
        station = next(s for s in stations if s.sta == data.sta)
        item = {
            'sta': data.sta,
            'staname': station.staname,
            'lon': float(station.lon),
            'lat': float(station.lat),
            'time': data.obs_hour.strftime('%Y-%m-%d %H:00'),
            'data': {}
        }
        # 按选择的要素返回数据
        if 'temp' in elements:
            item['data']['temp'] = float(data.temp) if data.temp else None
        if 'rain' in elements:
            item['data']['rain'] = float(data.rain) if data.rain else None
        if 'rh' in elements:
            item['data']['rh'] = data.rh if data.rh else None
        if 'press' in elements:
            item['data']['press'] = float(data.press) if data.press else None
        if 'wind' in elements:
            item['data']['wspeed'] = float(data.wspeed) if data.wspeed else None
            item['data']['wdirection'] = data.wdirection if data.wdirection else None
        if 'vis' in elements:
            item['data']['vis'] = float(data.vis) if data.vis else None
        result.append(item)

    return jsonify(result)


@bp.route('/api/get_area_boundary')
def get_area_boundary():
    area_name = request.args.get('area_name')
    # 从本地JSON中获取边界
    for feature in AREA_BOUNDARIES['features']:
        if feature['properties']['name'] == area_name:
            return jsonify(feature['geometry'])
    return jsonify({'error': '边界数据不存在'}), 404