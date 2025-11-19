from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Writer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    writerName = db.Column(db.String(100), nullable =False, unique=True)
    books = db.relationship('Book',backref='writer',lazy = True,cascade="all, delete-orphan")

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoryName = db.Column(db.String(100),nullable = False,unique = True)
    books = db.relationship('Book',backref='category',lazy=True,cascade="all, delete-orphan")
    def __repr__(self):
        return f'<Category {self.categoryName}>'

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookName = db.Column(db.String(200),nullable=False)
    writer_id = db.Column(db.Integer,db.ForeignKey('writer.id'),nullable=False)
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'),nullable=False)
    def __repr__(self):
        return f'<Book {self.bookName}>'