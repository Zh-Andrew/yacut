import re

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id

PATTERN_URL = re.compile(
    r'^(?:http|ftp)s?://'
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
    r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    r'(?::\d+)?'
    r'(?:/?|[/?]\S+)$', re.IGNORECASE
)
PATTERN_SHORT_URL = r'^[A-Za-z0-9]{1,16}$'


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if not data.get('url'):
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    if not re.match(PATTERN_URL, data['url']):
        raise InvalidAPIUsage('Ссылка не соответствует формату URL')
    if not data.get('custom_id'):
        data['custom_id'] = get_unique_short_id()
    if (
        data.get('custom_id') and
        URLMap.query.filter_by(short=data['custom_id']).first() is not None
    ):
        raise InvalidAPIUsage(f'Имя "{data.get("custom_id")}" уже занято.')
    if not re.match(PATTERN_SHORT_URL, data['custom_id']):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    url_obj = URLMap()
    url_obj.from_dict(data)
    db.session.add(url_obj)
    db.session.commit()
    return jsonify(url_obj.to_dict()), 201


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_url(short):
    original_link = URLMap.query.filter_by(short=short).first()
    if original_link is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': original_link.original}), 200
