from flask import Flask, render_template, request, redirect, url_for, flash
from data_models import db, Author, Book
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

#Define the base directory and database URI
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(base_dir, 'instance', 'library.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Initialize SQLAlchemy with the app
db.init_app(app)

#create the tables when the app starts
with app.app_context():
    db.create_all()  #create the tables if they don't exist

# Home route that displays all books in the database
@app.route('/')
def home():
    books = Book.query.all()  #fetch all books from the database
    return render_template('home.html', books=books)

#route to add a new author
@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form['name']
        birth_date = request.form['birth_date']
        date_of_death = request.form['date_of_death']

        #create a new Author object and add to the database
        author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)
        db.session.add(author)
        db.session.commit()

        flash('Author added successfully!', 'success')
        return redirect(url_for('add_author'))

    return render_template('add_author.html')

#route to add a new book
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        isbn = request.form['isbn']
        publication_year = request.form['publication_year']
        author_id = request.form['author_id']

        book = Book(title=title, isbn=isbn, publication_year=publication_year, author_id=author_id)
        db.session.add(book)
        db.session.commit()

        flash('Book added successfully!', 'success')
        return redirect(url_for('home'))
    #Fetch all authors to populate the author dropdown in the form
    authors = Author.query.all()  # Fetch all authors to display in the dropdown
    return render_template('add_book.html', authors=authors)


@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []  # Initialize an empty list to store search results
    if request.method == 'POST':
        search_query = request.form['search_query']

        # Perform a search by title, ISBN, or author name using the LIKE operator
        results = Book.query.filter(
            (Book.title.ilike(f'%{search_query}%')) |  # Search by book title
            (Book.isbn.ilike(f'%{search_query}%')) |  # Search by ISBN
            (Author.name.ilike(f'%{search_query}%'))  # Search by author's name
        ).join(Author).all()  # Join with Author table to get author data

    return render_template('search_results.html', results=results)

# Route to delete a book by ID
@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    author = book.author

    db.session.delete(book)
    db.session.commit()

    #if the author has no more books, delete the author
    if len(author.books) == 0:
        db.session.delete(author)
        db.session.commit()

    flash('Book deleted successfully!', 'success')
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
