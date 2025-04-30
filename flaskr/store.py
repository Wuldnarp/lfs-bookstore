from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('store', __name__)

@bp.route('/')
def index():
    db = get_db()
    books = db.execute(
        'SELECT p.id, title, price, sellerID, username'
        ' FROM book p JOIN user u ON p.sellerID = u.id'
    ).fetchall()
    return render_template('store/index.html', books=books)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO book (title, price, sellerID)'
                ' VALUES (?, ?, ?)',
                (title, price, g.user['id'])
            )
            db.commit()
            return redirect(url_for('store.index'))

    return render_template('store/create.html')

def get_book(id, check_author=True):
    book = get_db().execute(
        'SELECT p.id, title, price, sellerID, username'
        ' FROM book p JOIN user u ON p.sellerID = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if book is None:
        abort(404, f"book id {id} doesn't exist.")

    if check_author and book['sellerID'] != g.user['id']:
        abort(403)

    return book

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    book = get_book(id)

    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE book SET title = ?, price = ?'
                ' WHERE id = ?',
                (title, price, id)
            )
            db.commit()
            return redirect(url_for('store.index'))

    return render_template('store/update.html', book=book)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_book(id)
    db = get_db()
    db.execute('DELETE FROM book WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('store.index'))