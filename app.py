from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Book,Category, Writer
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gizli-anahtar'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir,"adminpanel.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

#Index ve modellerin listeleme işlemleri

@app.route('/')
def index():
    books = Book.query.all()
    categories = Category.query.all()
    writers = Writer.query.all()
    return render_template('index.html', books=books, categories=categories,writers = writers)

#Category CRUD işlemleri

@app.route('/category/add', methods=['GET', 'POST'])
def category_add():
    if request.method == 'POST':
        categoryName = request.form['categoryName'].strip()
        if categoryName:
            if Category.query.filter_by(categoryName=categoryName).first():
                flash('Bu kategori zaten mevcut!', 'danger')
            else:
                new_category = Category(categoryName=categoryName)
                db.session.add(new_category)
                db.session.commit()
                flash('Kategori eklendi!', 'success')
                return redirect(url_for('index'))
        else:
            flash('Kategori adı boş olamaz!', 'warning')
    return render_template('category_add.html')

@app.route('/category/update/<int:id>', methods=['GET', 'POST'])
def category_update(id):
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        new_categoryName = request.form['categoryName'].strip()
        if new_categoryName:
            if Category.query.filter(Category.categoryName == new_categoryName, Category.id != id).first():
                flash('Bu kategori adı zaten kullanılıyor!', 'danger')
            else:
                category.categoryName = new_categoryName
                db.session.commit()
                flash('Kategori güncellendi!', 'success')
                return redirect(url_for('index'))
        else:
            flash('Kategori adı boş olamaz!', 'warning')
    return render_template('category_update.html', category=category)

@app.route('/category/delete/<int:id>')
def category_delete(id):
    category = Category.query.get_or_404(id) 
    db.session.delete(category)
    db.session.commit()
    flash('Kategori ve bağlı kitapları silindi!', 'success')
    return redirect(url_for('index'))

#Book CRUD İşlemleri

@app.route('/book/add', methods=['GET', 'POST'])
def book_add():
    categories = Category.query.all()
    writers = Writer.query.all()
    if request.method == 'POST':
        bookName = request.form['bookName'].strip()
        category_id = request.form.get('category_id')
        writer_id = request.form.get('writer_id')
        if bookName  and category_id:
            newBook = Book(bookName=bookName, category_id=int(category_id),writer_id=int(writer_id))
            db.session.add(newBook)
            db.session.commit()
            flash('Kitap eklendi!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Tüm alanlar doldurulmalıdır!', 'warning')
    return render_template('book_add.html', categories=categories,writers = writers)

@app.route('/book/update/<int:id>', methods=['GET', 'POST'])
def book_update(id):
    book = Book.query.get_or_404(id)
    categories = Category.query.all()
    if request.method == 'POST':
        bookName = request.form['bookName'].strip()
        writer_id = request.form.get('writer_id')
        category_id = request.form.get('category_id')
        if bookName and category_id:
            book.bookName = bookName
            book.writer_id = int(writer_id)
            book.category_id = int(category_id)
            db.session.commit()
            flash('Kitap güncellendi!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Tüm alanlar doldurulmalıdır!', 'warning')
    return render_template('book_update.html', book=book, categories=categories)

@app.route('/book/delete/<int:id>')
def book_delete(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash('Kitap silindi!', 'success')
    return redirect(url_for('index'))

#Writer CRUD İşlemleri

@app.route('/writer/add', methods=['GET', 'POST'])
def writer_add():
    if request.method == 'POST':
        writerName = request.form['writerName'].strip()
        if writerName:
            if Writer.query.filter_by(writerName=writerName).first():
                flash('Bu yazar zaten mevcut!', 'danger')
            else:
                new_writer = Writer(writerName=writerName)
                db.session.add(new_writer)
                db.session.commit()
                flash('Yazar eklendi!', 'success')
                return redirect(url_for('index'))
        else:
            flash('Yazar adı boş olamaz!', 'warning')
    return render_template('writer_add.html')

@app.route('/writer/update/<int:id>', methods=['GET', 'POST'])
def writer_update(id):
    writer = Writer.query.get_or_404(id)
    if request.method == 'POST':
        new_writerName = request.form['writerName'].strip()
        if new_writerName:
            if Writer.query.filter(Writer.writerName == new_writerName, Writer.id != id).first():
                flash('Bu yazar zaten kullanılıyor!', 'danger')
            else:
                writer.writerName = new_writerName
                db.session.commit()
                flash('Yazar güncellendi!', 'success')
                return redirect(url_for('index'))
        else:
            flash('Yazar adı boş olamaz!', 'warning')
    return render_template('writer_update.html', writer=writer)

@app.route('/writer/delete/<int:id>')
def writer_delete(id):
    writer = Writer.query.get_or_404(id) 
    db.session.delete(writer)
    db.session.commit()
    flash('Yazar ve bağlı kitapları silindi!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)