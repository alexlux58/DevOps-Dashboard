
from app import create_app

# Create the Flask app by calling the 'create_app' function
app = create_app()

# Run the Flask application in debug mode if the script is executed directly
if __name__ == '__main__':
    app.run(debug=True)
