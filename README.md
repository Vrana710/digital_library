# Digital Library

Welcome to the Digital Library project! This application allows users to manage their book collection, including adding books, authors, searching through the collection, and getting book recommendations. It is built using Flask and Flask-SQLAlchemy with an SQLite database.

## Features

- Add and manage authors
- Add and manage books
- Search for books by title and author name
- Sort books by title, author, or publication year
- Display books with their authors on the homepage
- Get book recommendations
- Update and delete books and authors
- Flash messages for user feedback

## Setup Instructions

### Prerequisites

- Python 3.x
- pip (Python package installer)

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Vrana710/digital_library.git
   cd digital_library
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Required Packages**

   ```bash
   pip3 install -r requirements.txt
   ```

   *Note:* Ensure your `requirements.txt` file contains dependencies such as `flask`, `requests`,`flask_sqlalchemy`, and `jinja2`.

4. **Setup the Database**

   You can create the SQLite database automatically when you start the application:

   ```bash
   python3 app.py
   ```

   This will initialize the Flask app and create the necessary database tables if they don't exist.

### Running the Application

1. **Start the Flask Development Server**

   ```bash
   python3 app.py
   ```

2. **Access the Application**

   Open your web browser and navigate to `http://127.0.0.1:5000/`.

### Usage

- **Add Authors:** Navigate to `/add_author` to add new authors to the library.
- **Add Books:** Navigate to `/add_book` to add new books, linking them to authors.
- **Book Recommendations:** Click on the "Get Book Recommendations" button for suggested readings.
- **Search Books:** Use the search bar on the homepage to find books by title or author name.
- **Sort Books:** Sort books by title, author name, or publication year.
- **Update Books and Authors:** Edit book or author details by clicking on the "Edit" button next to their name.
- **Delete Books:** Remove books using the "Delete" button next to the book.
- **Delete Authors:** Remove authors (and their associated books) using the delete button next to the author's name.

### Templates

- `home.html`: Displays a list of books with authors and provides options for searching, sorting, updating, and deleting.
- `add_author.html`: Form for adding new authors.
- `add_book.html`: Form for adding new books.
- `update_author.html`: Form for updating existing authors.
- `update_book.html`: Form for updating existing books.
- `recommendations.html`: Displays recommendations for books

### Bonus Features (Optional)

- **UI Redesign:** Customize the user interface using Bootstrap and custom styles.
- **Detail Pages:** Implement detail pages to view more information about specific books or authors.
- **Book Ratings:** Introduce a rating system for books to enhance the user experience.
- **AI-based Book Recommendations:** Integrate AI algorithms to provide book recommendations based on the user's collection or preferences.

### Contributing

Feel free to contribute to this project by submitting issues or pull requests. Ensure that your code adheres to the project's coding standards and includes relevant documentation.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or suggestions, feel free to contact me at [ranavarsha710@gmail.com](mailto:ranavarsha710@gmail.com).
