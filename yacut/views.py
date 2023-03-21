import random
import string

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import YacutForm
from .models import URLMap


def get_unique_short_id():
    seq = string.ascii_letters + string.digits
    return ''.join((random.choice(seq)) for _ in range(6))


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = YacutForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        if not short:
            short = get_unique_short_id()
        if URLMap.query.filter_by(short=short).first() is not None:
            form.custom_id.errors = [f'Имя {short} уже занято!', ]
            return render_template('yacut.html', form=form)
        short_id = URLMap(
            original=form.original_link.data,
            short=short
        )
        db.session.add(short_id)
        db.session.commit()
        flash(url_for("short_view", short=short, _external=True))
    return render_template('yacut.html', form=form)


@app.route('/<string:short>')
def short_view(short):
    original = URLMap.query.filter_by(short=short).first_or_404().original
    if original is not None:
        return redirect(original)
    abort(404)
