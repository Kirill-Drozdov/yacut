from flask import jsonify, request

from yacut import app, db
from yacut.views import get_unique_short_id
from yacut.models import URLMap
from yacut.error_handlers import InvalidAPIUsage


@app.route('/api/id/', methods=['POST'])
def create_id_view():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    custom_id = data.get('custom_id')
    if custom_id is None or custom_id == '':
        custom_id = get_unique_short_id()
        data['custom_id'] = custom_id
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if URLMap.query.filter_by(short=custom_id).first() is not None:
        raise InvalidAPIUsage(f'Имя "{custom_id}" уже занято.')
    if len(custom_id) > 16:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    url = URLMap()
    url.from_dict(data)
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict()), 201


@app.route('/api/id/<path:short_id>/', methods=['GET'])
def get_url_view(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url is not None:
        return jsonify({'url': url.original}), 200
    raise InvalidAPIUsage('Указанный id не найден', 404)
