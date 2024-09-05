from app import app, db

with app.app_context():
    """
    Initializes the application context and creates the database tables.

    This script ensures that all the tables defined in the SQLAlchemy models
    are created in the database. It should be run when setting up the
    application for the first time or when new models are added.

    Actions:
        - Creates all tables defined in the app's models using SQLAlchemy's
          `create_all()` method.
        - Prints a confirmation message when the tables are successfully created.

    Note:
        This script assumes that the database configurations and models are
        properly set up in the `app` module.

    """
    db.create_all()
    print("Database tables created.")
