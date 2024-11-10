from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.sqlite'
app.secret_key = 'your_secret_key'  # Necessary for flashing messages
db.init_app(app)

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form['name']
        birth_date = request.form['birth_date']
        date_of_death = request.form['date_of_death']

        # Create a new Author object
        new_author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)

        # Add the author to the database
        db.session.add(new_author)
        db.session.commit()

        flash('Author added successfully!', 'success')
        return redirect(url_for('add_author'))  # Redirect to the same page to see the success message

    return render_template('add_author.html')  # Renders the form


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        isbn = request.form['isbn']
        publication_year = request.form['publication_year']
        author_id = request.form['author_id']  # Get the selected author ID

        # Create a new Book object
        new_book = Book(title=title, isbn=isbn, publication_year=publication_year, author_id=author_id)

        # Add the book to the database
        db.session.add(new_book)
        db.session.commit()

        flash('Book added successfully!', 'success')
        return redirect(url_for('home'))  # Redirect to home page after adding the book

    authors = Author.query.all()  # Get all authors from the database
    return render_template('add_book.html', authors=authors)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    # Find the book by its ID
    book = Book.query.get_or_404(book_id)

    # Check if the book's author has other books
    author = book.author
    author_books_count = Book.query.filter_by(author_id=author.id).count()

    # Delete the book
    db.session.delete(book)

    # If the author has no other books, delete the author as well
    if author_books_count == 1:
        db.session.delete(author)

    # Commit the changes to the database
    db.session.commit()

    # Redirect to the homepage with a success message
    flash(f"Book '{book.title}' was successfully deleted!", 'success')
    return redirect(url_for('home'))


@app.route('/')
def home():
    search_query = request.args.get('search', '')  # Get search query from the URL
    sort_by = request.args.get('sort_by', 'title')  # Default sort by title

    # Handle sorting and filtering
    if sort_by == 'author':
        # Search books by title and sort by author's name
        books = Book.query.join(Author).filter(Book.title.like(f'%{search_query}%')).order_by(Author.name).all()
    else:
        # Default sort by title
        books = Book.query.filter(Book.title.like(f'%{search_query}%')).order_by(Book.title).all()

    # Pass the actual Book objects to the template
    return render_template('home.html', books=books)


def seed_data():
    # Clear existing data to avoid duplication
    Author.query.delete()
    Book.query.delete()

    # Convert string dates into datetime.date objects
    author1 = Author(name='J.K. Rowling', birth_date=datetime(1965, 7, 31).date())
    author2 = Author(name='George R.R. Martin', birth_date=datetime(1948, 9, 20).date())
    author3 = Author(name='J.R.R. Tolkien', birth_date=datetime(1892, 1, 3).date())

    # Add books associated with authors
    book1 = Book(title="Harry Potter and the Sorcerer's Stone", isbn='9780439708180', publication_year=1997, author=author1)
    book2 = Book(title='A Game of Thrones', isbn='9780553593716', publication_year=1996, author=author2)
    book3 = Book(title='The Hobbit', isbn='9780547928227', publication_year=1937, author=author3)

    # Add and commit to the database
    db.session.add_all([author1, author2, author3, book1, book2, book3])
    db.session.commit()
    print("Database seeded successfully!")



with app.app_context():
    db.create_all()  # Create tables if they don't exist
    seed_data()


if __name__ == '__main__':
    app.run(debug=True)