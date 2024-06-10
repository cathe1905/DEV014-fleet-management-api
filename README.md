Taxi Data API 🚖

This is a Flask-based RESTful API that provides access to taxi and trajectory data. The API allows users to retrieve information about taxis, trajectories, and users, as well as to perform operations such as creating, updating, and deleting user records.
Technologies Used 🛠️

Flask: A lightweight Python web framework used for building the API endpoints. SQLAlchemy: An SQL toolkit and Object-Relational Mapping (ORM) library for Python, used for interacting with the database. JWT (JSON Web Tokens): Used for authentication and authorization of users. Pandas: A powerful data manipulation library in Python, used for processing and exporting data to Excel.Python-dotenv: A Python module that reads the key-value pairs from a .env file and sets them as environment variables.

API Overview 📋

The API provides the following endpoints:

    /taxis: Retrieve taxi data with optional pagination and filtering by query string.
    /trajectories/{taxi_id}: Retrieve trajectory data for a specific taxi by providing the taxi ID.
    /trajectories/latest: Retrieve the latest trajectory data for all taxis.
    /users: Perform CRUD operations on user records.
    /auth/login: Authenticate users and generate JWT tokens.
    /trajectories/export: Export taxi data to an Excel file and send it via email.

CLI Tool for Data Conversion and Insertion 🛠️

    Alongside the RESTful API, the project features a CLI tool using Pandas. This tool streamlines the conversion of text files into DataFrame objects and their insertion into the database. It automates data import tasks for enhanced efficiency.

Comprehensive Testing with UnitTest and PyTest 🧪

    Extensive testing, employing both UnitTest and PyTest frameworks, ensures the reliability of the application. Tests cover endpoint responses, database operations, error handling, and more, ensuring stability and facilitating future enhancements.

How It Works ℹ️

    Authentication: Users can authenticate using their email and password to obtain a JWT token.
    Endpoints: Users can access various endpoints to retrieve, create, update, or delete data.
    Data Export: The /trajectories/export endpoint allows users to export taxi data to an Excel file and send it via email.
    Error Handling: The API handles various errors such as invalid requests or internal server errors and provides appropriate error messages.

Running the API 🏃‍♂️

To run the API locally:

    Clone this repository.
    Install the required dependencies using pip install -r requirements.txt.
    Set up the database connection URI and other environment variables in a .env file.
    Run the Flask application using python app.py.
    Access the API endpoints using an HTTP client like Postman or cURL.

Contribution Guidelines 🤝

Contributions to improve the API are welcome! Please follow the standard guidelines for contributing and make sure to test your changes thoroughly before submitting a pull request.
