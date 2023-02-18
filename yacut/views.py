from flask import render_template, redirect, flash, url_for

from yacut import app, db
from yacut.forms import URLForm
from yacut.models import URLMap


@app.route('/', methods=['GET', 'POST'])
def add_url_view():
    form = URLForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        if URLMap.query.filter_by(short=short).first():
            flash('Такая короткая ссылка уже существует!')
            return render_template('add_url.html', form=form)
        url = URLMap(
            original=form.original_link.data,
            short=form.custom_id.data,
        )
        db.session.add(url)
        db.session.commit()
        return render_template('add_url.html', form=form)
    return render_template('add_url.html', form=form)


@app.route('/<path:custom_id>')
def redirect_view(custom_id):
    url = URLMap.query.filter_by(short=custom_id).first()
    original = url.original
    return redirect(original)
