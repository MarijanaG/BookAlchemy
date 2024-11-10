from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    date_of_death = db.Column(db.Date, nullable=True)


    def __repr__(self):
        # debug method
        return f"<Author(id={self.id}, name='{self.name}', birth_date={self.birth_date}, date_of_death={self.date_of_death})>"


    def __str__(self):
        # display what is inside
        return f"{self.name} (Born: {self.birth_date}, Died: {self.date_of_death})"


class Book(db.Model):
    __tablename__= "books"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(20), nullable=False, unique=True)
    title = db.Column(db.String(200), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)

    author = db.relationship('Author', backref='books')

    def __repr__(self):
        # debug method
        return f"<Book(id={self.id}, title='{self.title}', isbn='{self.isbn}', publication_year={self.publication_year}, author_id={self.author_id})>"

    def __str__(self):
        # display what is inside
        return f"{self.title} (ISBN: {self.isbn}, Year: {self.publication_year}, Author ID: {self.author_id})"