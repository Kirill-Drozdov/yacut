import string
from random import randrange

from flask import abort, render_template, redirect, flash
from yacut import app, db
from yacut.constants import ADD_URL_HTML
from yacut.forms import URLForm
from yacut.models import URLMap


def get_unique_short_id():
    base_string = string.ascii_letters + string.digits
    short_url = ''.join([
        base_string[randrange(len(base_string))] for i in range(6)
    ])
    if URLMap.query.filter_by(short=short_url).first():
        return get_unique_short_id()
    return short_url


@app.route('/', methods=['GET', 'POST'])
def add_url_view():
    form = URLForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        # Если пользователь не ввёл свой вариант короткой ссылки.
        if not short:
            short = get_unique_short_id()
            form.custom_id.data = short

        if URLMap.query.filter_by(short=short).first():
            flash(f'Имя {short} уже занято!')
            return render_template(ADD_URL_HTML, form=form)
        url = URLMap(
            original=form.original_link.data,
            short=short,
        )
        db.session.add(url)
        db.session.commit()
        return render_template(ADD_URL_HTML, form=form)
    return render_template(ADD_URL_HTML, form=form)


@app.route('/<path:custom_id>')
def redirect_view(custom_id):
    url = URLMap.query.filter_by(short=custom_id).first()
    if url is not None:
        original = url.original
        return redirect(original)
    abort(404)
