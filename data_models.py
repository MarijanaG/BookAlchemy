from flask_sqlalchemy import SQLAlchemy

#creating an instance of SQLAlchemy for interacting with the database
db = SQLAlchemy()


#author model represents authors in the database
class Author(db.Model):
    __tablename__ = 'author'
    # id is the primary key for each author, it is automatically incremented
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    #birth_date and date_of_death are optional fields to store dates as strings
    birth_date = db.Column(db.String(10))
    date_of_death = db.Column(db.String(10))

    # __repr__ method is used to provide a string representation of the object
    def __repr__(self):
        return f'<Author {self.name}>'


#book model represents books in the database
class Book(db.Model):
    __tablename__ = 'book'

    #id is the primary key for each book, it is automatically incremented
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(13), nullable=False, unique=True)
    #title is a string column that stores the book's title and cannot be null
    title = db.Column(db.String(255), nullable=False)
    publication_year = db.Column(db.Integer)
    #author_id is a foreign key that links to the Author model's id
    #This establishes a relationship between the Book and Author models
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

    # author creates a relationship between Book and Author models
    # It allows easy access to the author's details from a book object
    author = db.relationship('Author', backref=db.backref('books', lazy=True))

    # __repr__ method is used to provide a string representation of the book
    def __repr__(self):
        return f'<Book {self.title}>'
