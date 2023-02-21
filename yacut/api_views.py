from http import HTTPStatus

from flask import jsonify, request

from yacut import app, db
from yacut.views import get_unique_short_id
from yacut.models import URLMap
from yacut.error_handlers import InvalidAPIUsage
from yacut.validators import validate_short_url


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
    if not validate_short_url(custom_id):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    url = URLMap()
    url.from_dict(data)
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<path:short_id>/', methods=['GET'])
def get_url_view(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url is not None:
        return jsonify({'url': url.original}), HTTPStatus.OK
    raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
