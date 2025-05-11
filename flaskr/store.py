from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
from datetime import datetime
from flaskr.informationFlow import (Confidentiality,Role,can_flow,declassify)
bp = Blueprint('store', __name__)

@bp.route('/')
def index():

    if not can_flow(Confidentiality.LOW, Role.UNREGISTERED,Confidentiality.LOW, Role.UNREGISTERED):
        raise Exception("illegal information flow")
    
    db = get_db()
    books = db.execute(
        'SELECT p.id, title, author, year, edition, publisher, condition, description, price, sellerID, username'
        ' FROM book p JOIN user u ON p.sellerID = u.id'
    ).fetchall()
    return render_template('store/index.html', books=books)

@bp.route('/search', methods=('GET', 'POST'))
def search():

    if not can_flow(Confidentiality.LOW, Role.UNREGISTERED,Confidentiality.LOW, Role.UNREGISTERED):
        raise Exception("illegal information flow")

    if request.method == 'POST':
        search_value = request.form['search']

        results = get_db().execute(
            "SELECT * FROM book p JOIN user u ON p.sellerID = u.id WHERE title LIKE ? OR author LIKE ? OR year LIKE ? OR edition LIKE ? OR publisher LIKE ? OR condition LIKE ? OR description LIKE ? OR price LIKE ? OR username LIKE ? ",
            ('%' + search_value + '%',) * 9
        ).fetchall()
        return render_template('store/search.html', results=results)

    return render_template('store/search.html')


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':

        if not declassify(Confidentiality.LOW, Role.SELLER, Confidentiality.LOW, Role.UNREGISTERED):
            raise Exception("illegal declassification")

        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        edition = request.form['edition']
        publisher = request.form['publisher']
        condition = request.form['condition']
        description = request.form['description']
        price = request.form['price']

        error = None

        if not title or not author or not year or not edition or not publisher or not condition or not description or not price:
            error = 'missing some information.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO book (title, author, year, edition, publisher, condition, description, price, sellerID)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (title, author, year, edition, publisher, condition, description, price, g.user['id'])
            )
            db.commit()
            return redirect(url_for('store.index'))

    return render_template('store/create.html')

@bp.route('/transactions')
@login_required
def transactions():
    db = get_db()
    transactions = db.execute(
        'SELECT p.date, p.address, b.title, b.author, b.year, b.edition, b.publisher, b.condition, b.description, b.price, u.username '
        'FROM purchase p '
        'INNER JOIN book b ON p.bookID = b.id '
        'INNER JOIN user u on b.sellerID = u.ID '
        'WHERE p.buyerID = ?'
        'ORDER BY p.date DESC',
        (g.user['id'],)
    ).fetchall()
    return render_template('store/transactions.html', transactions=transactions)

def get_book(id, check_author=True):
    book = get_db().execute(
        'SELECT p.id, title, author, year, edition, publisher, condition, description, price, sellerID, username'
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
        author = request.form['author']
        year = request.form['year']
        edition = request.form['edition']
        publisher = request.form['publisher']
        condition = request.form['condition']
        description = request.form['description']
        price = request.form['price']

        error = None

        if not title or author or year or edition or publisher or condition or description or price:
            error = 'missing some information.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE book SET title = ?, author = ?, year = ?, edition = ?, publisher = ?, condition = ?, description = ?, price = ?'
                ' WHERE id = ?',
                (title, author, year, edition, publisher, condition, description, price, id)
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

@bp.route('/<int:id>/purchase', methods=('GET', 'POST'))
@login_required
def purchase(id):
    book = get_book(id, False)

    if request.method == 'POST':

        if not can_flow(Confidentiality.LOW, Role.UNREGISTERED,Confidentiality.HIGH, Role.BUYER):
            raise Exception("illegal information flow")
    
        address = request.form['address']

        db = get_db()

        status = db.execute(
            "SELECT 1 FROM purchase WHERE bookID = ? LIMIT 1",
            (id,)
        ).fetchone()

        if (status is not None):
            flash('This book is already sold')
            return redirect(url_for('index'))
        
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        db.execute(
            'INSERT INTO purchase (bookID, date, address, buyerID )'
            ' VALUES (?,?,?,?)',
            (book['id'], created_at, address, g.user['id'])
        )
        db.commit()

        return redirect(url_for('store.transactions'))

    return render_template('store/purchase.html', book=book)