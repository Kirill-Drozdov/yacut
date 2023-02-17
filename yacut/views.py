from flask import render_template, redirect, flash, url_for

from yacut import app, db
from yacut.forms import URLForm
from yacut.models import URLMap


@app.route('/', methods=['GET', 'POST'])
def add_url_view():
    form = URLForm()
    if form.validate_on_submit():
        short = form.short.data
        original = form.original.data
        if URLMap.query.filter_by(short=short).first():
            flash('Такая короткая ссылка уже существует!')
            return render_template('add_url.html', form=form)
        elif URLMap.query.filter_by(original=original).first():
            flash('Такая длинная ссылка уже существует!')
            return render_template('add_url.html', form=form)
        url = URLMap(
            original=form.original.data,
            short=form.short.data,
        )
        db.session.add(url)
        db.session.commit()
        return render_template('add_url.html', form=form)
        # return redirect(url_for('url_detail_view', id=url.id))
    return render_template('add_url.html', form=form)


@app.route('/<path:short>')
def redirect_view(short):
    url = URLMap.query.filter_by(short=short).first()
    original = url.original
    return redirect(original)
