from flask import render_template, flash

from yacut import app, db
from yacut.forms import URLForm
from yacut.models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        short = form.short.data
        original = form.original.data
        if URLMap.query.filter_by(short=short).first():
            flash('Такая короткая ссылка уже существует!')
            return render_template('index.html', form=form)
        elif URLMap.query.filter_by(original=original).first():
            flash('Такая длинная ссылка уже существует!')
            return render_template('index.html', form=form)
        url = URLMap(
            original=form.original.data,
            short=form.short.data,
        )
        db.session.add(url)
        db.session.commit()
        return render_template('index.html', form=form)
    return render_template('index.html', form=form)