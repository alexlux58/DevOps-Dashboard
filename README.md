# DevOps-Project

# Flask App

## Description

This repository contains a web application with some Flask routes for user authentication and account management. The application uses Flask, SQLAlchemy, and Flask-Login to provide a basic user registration and login system.

## Getting Started

To get started with this Flask app, follow the steps below:

1. Clone the repository to your local machine:

git clone https://github.com/alexlux58/DevOps-Project.git

2. Install the required dependencies. It's recommended to use a virtual environment:

cd your_project
python -m venv venv
source venv/bin/activate (for Windows: venv\Scripts\activate)
pip install -r requirements.txt

3. Set up the database:

The application uses SQLite as the database for storing user information. The default database file name is `database.db`, but you can change it by modifying the `DB_NAME_USERS` variable in `app.py`.

4. To run the application and create the necessary database tables, run the following command:

python app.py

By default, the application runs on `http://127.0.0.1:5000/`.

## Routes

### /logout

This route handles user logout. It requires the user to be logged in. When accessed, it performs the following actions:

- Displays a success message using the flash function: "Account Logged Out!"
- Logs out the current user using the logout_user() function.
- Redirects the user to the login page.

### /sign-up

This route handles user sign-up. It supports both GET and POST methods. When accessed with a GET request, it renders the "sign_up.html" template. When accessed with a POST request, it performs the following actions:

- Retrieves user information from the form data (email, firstName, lastName, password, verifyPassword).
- Queries the database to check if a user with the same email already exists. If found, it displays an error message using the flash function: "Email already exists."
- Checks if the email length is less than 4 characters and presumably displays some error handling (the code snippet provided is incomplete, and the else block is not included).

## Note

This README.md file provides only a brief description of the routes and their functionalities. To run the web application successfully, you need to ensure that you have set up the Flask environment and the required database configuration.

## Disclaimer

The code snippet provided is incomplete, and there might be missing parts or potential errors. Make sure to review and complete the code before using it in production.

## Project Structure

The main components of the Flask app are organized as follows:

- `app.py`: The entry point of the application. It contains the Flask app setup, database initialization, blueprints registration, and login manager configuration.

- `app/models.py`: Defines the `User` model that represents the user table in the database.

- `app/views.py`: Contains the main views (routes) for rendering HTML templates and handling user interactions.

- `app/auth.py`: Handles user authentication, including login, logout, and registration.

- `templates/`: Contains HTML templates used for rendering the app's web pages.

- `static/`: Stores static assets like CSS, JavaScript, and images.

## License

This project is licensed under the [MIT License](LICENSE).

Feel free to modify and use this code for your own projects!

## Contributions

Contributions to this project are welcome. If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## Acknowledgments

This Flask app is based on the [Flask](https://flask.palletsprojects.com/) micro web framework, [SQLAlchemy](https://www.sqlalchemy.org/) for database interactions, and [Flask-Login](https://flask-login.readthedocs.io/) for handling user sessions.

## Contact

If you have any questions or need further assistance, you can contact me at your_email@example.com.

Happy coding!
