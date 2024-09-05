import os
import time
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

import requests  # For calling external AI API

from data_models import db, Author, Book


app = Flask(__name__)

# Correct the file path construction
file_path = os.path.join(os.getcwd(), "data", "library.sqlite")

app.config['SECRET_KEY'] = 'vrana710@2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    Add a new author to the database.

    If the request method is POST:
        Validates the input from the form.
        Checks if the author already exists.
        If not, creates a new Author object and adds it to the database.

    Returns:
        str: Rendered HTML template with success or error message.
    """
    success_message = ""
    if request.method == 'POST':
        name = request.form['name']
        birth_date_str = request.form['birth_date']
        date_of_death_str = request.form['date_of_death']

        # Validate input
        if not name or not birth_date_str:
            return "Name and birth date are required."

        try:
            birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
            date_of_death = datetime.strptime(date_of_death_str, 
                                              '%Y-%m-%d').date() if date_of_death_str else None
        except ValueError:
            return "Incorrect date format. Please use yyyy-mm-dd."

        # Check if the Author already exists
        existing_author = Author.query.filter_by(name=name).first()
        if existing_author:
            error_message = f"Author '{name}' already exists."
            return render_template('add_author.html', error_message=error_message)

        # Create Author object and add to database
        new_author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)
        db.session.add(new_author)
        db.session.commit()

        # Success message
        success_message = f"Author '{name}' successfully added."
        return render_template('add_author.html', success_message=success_message)

    return render_template('add_author.html', success_message=success_message)


@app.route('/add_book', methods=['GET', 'POST'])
def add_book_page():
    """
    Display the add book form and handle form submission.

    If the request method is POST:
        Validates the input from the form.
        Checks if the book already exists.
        If not, creates a new Book object and adds it to the database.

    Returns:
        str: Rendered HTML template with success or error message.
    """
    authors = Author.query.all()
    if request.method == 'POST':
        isbn = request.form['isbn']
        title = request.form['title']
        publication_year = request.form['publication_year']
        author_id = request.form['author_id']
        rating = request.form.get('rating')  # Get rating from form

        # Validate input
        if not (isbn and title and publication_year and author_id):
            flash("Please fill out all fields correctly.", 'danger')
            return render_template('add_book.html', authors=authors)

        # Check if the ISBN already exists
        existing_book = Book.query.filter_by(isbn=isbn).first()
        if existing_book:
            flash(f"Book with ISBN '{isbn}' already exists.", 'danger')
            return render_template('add_book.html', authors=authors)

        # Create Book object and add to database
        new_book = Book(isbn=isbn, 
                        title=title, 
                        publication_year=publication_year, 
                        author_id=author_id, 
                        rating=rating)
        db.session.add(new_book)
        db.session.commit()

        flash(f"Book '{title}' successfully added.", 'success')
        return redirect(url_for('home_page'))

    return render_template('add_book.html', authors=authors)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """
    Delete a book from the database.

    Args:
        book_id (int): The ID of the book to delete.

    Returns:
        redirect: Redirects to the home page.
    """
    book = Book.query.get_or_404(book_id)
    author_id = book.author_id

    try:
        db.session.delete(book)
        db.session.commit()

        # Check if the author has no other books
        author = Author.query.get(author_id)
        if author and not author.books:
            db.session.delete(author)
            db.session.commit()

        flash(f"Book '{book.title}' has been successfully deleted.", 'success')
    except:
        flash(f"An error occurred while deleting the book '{book.title}'.", 'danger')

    return redirect(url_for('home_page'))


@app.route('/')
def home_page():
    """
    Display the home page with a list of books.

    Query parameters:
        sort_by (str): Sorts books by 'title', 'author', 'published_oldest',
            'published_newest', or 'title_reverse'. Default is 'title'.
        search (str): Filters books by title or author name containing the search term.

    Returns:
        str: Rendered HTML template with list of books, authors, and message.
    """
    sort_by = request.args.get('sort_by', 'title')  # Default sort by title
    search_term = request.args.get('search', '')

    # Determine sorting order
    if sort_by == 'author':
        books = Book.query.join(Author).order_by(Author.name).all()
    elif sort_by == 'published_oldest':
        books = Book.query.order_by(Book.publication_year).all()
    elif sort_by == 'published_newest':
        books = Book.query.order_by(desc(Book.publication_year)).all()
    elif sort_by == 'title_reverse':
        books = Book.query.order_by(desc(Book.title)).all()
    else:
        books = Book.query.order_by(Book.title).all()

    # Search filter
    if search_term:
        # Check if search term matches book title or author name
        books = Book.query.join(Author).filter(
            (Book.title.ilike(f'%{search_term}%')) | 
            (Author.name.ilike(f'%{search_term}%'))
        ).all()
        
        if not books:
            message = f"No books found matching '{search_term}'."
        else:
            message = f"Books matching '{search_term}':"
    else:
        message = "All books:"

    # Get all authors for display or use in other parts of the page
    authors = Author.query.all()
    return render_template('home.html', 
                           books=books, 
                           authors=authors, 
                           sort_by=sort_by, 
                           message=message)


@app.route('/update_author/<int:author_id>', methods=['GET', 'POST'])
def update_author(author_id):
    """
    Update an existing author in the database.

    Args:
        author_id (int): The ID of the author to update.

    Returns:
        str: Rendered HTML template with updated author details or error messages.
            If the request method is POST, returns a redirect to the home page.

    Raises:
        None

    """
    author = Author.query.get_or_404(author_id)
    if request.method == 'POST':
        name = request.form['name']
        birth_date_str = request.form['birth_date']
        date_of_death_str = request.form['date_of_death']

        # Validate input
        if not name or not birth_date_str:
            flash("Name and birth date are required.", 'danger')
            return render_template('update_author.html', author=author)

        try:
            birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
            date_of_death = datetime.strptime(date_of_death_str, 
                                              '%Y-%m-%d').date() if date_of_death_str else None
        except ValueError:
            flash("Incorrect date format. Please use yyyy-mm-dd.", 'danger')
            return render_template('update_author.html', author=author)

        # Update author details
        author.name = name
        author.birth_date = birth_date
        author.date_of_death = date_of_death

        db.session.commit()
        flash(f"Author '{name}' successfully updated.", 'success')
        return redirect(url_for('home_page'))

    return render_template('update_author.html', author=author)


@app.route('/update_book/<int:book_id>', methods=['GET', 'POST'])
def update_book(book_id):
    """
    Update an existing book in the database.

    Args:
        book_id (int): The ID of the book to update.

    Returns:
        str: Rendered HTML template with updated book details or error messages.
            If the request method is POST, returns a redirect to the home page.

    Raises:
        None

    """
    book = Book.query.get_or_404(book_id)
    authors = Author.query.all()

    if request.method == 'POST':
        isbn = request.form['isbn']
        title = request.form['title']
        publication_year = request.form['publication_year']
        author_id = request.form['author_id']

        # Validate input
        if not (isbn and title and publication_year and author_id):
            flash("Please fill out all fields correctly.", 'danger')
            return render_template('update_book.html', 
                                   book=book, 
                                   authors=authors)

        # Update book details
        book.isbn = isbn
        book.title = title
        book.publication_year = publication_year
        book.author_id = author_id

        db.session.commit()
        flash(f"Book '{title}' successfully updated.", 'success')
        return redirect(url_for('home_page'))

    return render_template('update_book.html', 
                           book=book, 
                           authors=authors)


@app.route('/author/<int:author_id>/delete', methods=['POST'])
def delete_author(author_id):
    """
    Deletes an author and their associated books from the database.

    Args:
        author_id (int): The unique identifier of the author to delete.

    Returns:
        redirect: A redirect to the home page after the deletion operation.

    Raises:
        None

    """
    author = Author.query.get_or_404(author_id)
    try:
        db.session.delete(author)
        db.session.commit()
        flash(f"Author '{author.name}' and their books have been successfully deleted.", 'success')
    except:
        flash(f"An error occurred while deleting the author '{author.name}'.", 'danger')
    return redirect(url_for('home_page'))


@app.route('/recommendations')
def recommendations():
    """
    Fetches and displays a list of random horror books from an external API.

    Makes a GET request to the RapidAPI endpoint for fetching ebooks in the horror genre.
    Implements a retry mechanism in case of failures or timeouts.

    URL and headers for the RapidAPI request are defined within the function.
    Retry settings are also defined, including the maximum number of 
    retries and the delay between retries.

    The function initializes an empty list to store the fetched books.
    It then iterates over the retry attempts, making the API request 
    and handling any exceptions that occur.
    If the request is successful (status code 200), the API response 
    is directly assigned to the random_books list.
    If the request fails or times out, appropriate error messages 
    are displayed using Flask's flash function.

    After all retry attempts or successful API response, 
    the function renders the recommendations template,
    passing the random_books list as a parameter.

    Returns:
        str: Rendered HTML template with a list of random horror books.
    """
    # URL and headers for RapidAPI request
    api_url = "https://freebooks-api2.p.rapidapi.com/fetchEbooks/horror"
    headers = {
        "x-rapidapi-host": "freebooks-api2.p.rapidapi.com",
        "x-rapidapi-key": "86f8b0591fmshfe9efe48ca0a473p1ff713jsnd95e46c20fac"
    }

    # Define retry settings
    max_retries = 3
    retry_delay = 2  # seconds

    random_books = []  # Initialize an empty list

    for attempt in range(max_retries):
        try:
            # Make the API request to fetch random books
            response = requests.get(api_url, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                # The API returns a list, so directly assign the response to random_books
                random_books = response.json()
                break
            else:
                flash(f"Failed to fetch recommendations: {response.status_code}", 'danger')
        except Exception as e:
            flash(f"An error occurred while fetching recommendations: {e}", 'danger')

        # Retry after a delay if it's not the last attempt
        if attempt < max_retries - 1:
            time.sleep(retry_delay)

    # Render the recommendations template, even if the list is empty
    return render_template('recommendations.html', books=random_books)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
