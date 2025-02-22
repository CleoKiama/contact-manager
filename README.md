# Flask-Mongo Contact Manager

This repository contains a web application built using the Flask framework and MongoDB. The application allows users to register and log in, reset their passwords via email, and manage contact details. Contacts include mobile phone number, email, address, and registration number. Additionally, the application provides a search functionality that allows users to search for contacts based on their registration number.

## Features

- **User Authentication**
  - Login page with username and password.
  - "Forgot Password" functionality that sends a reset email to the user.
- **Contact Details Management**

  - Form for users to enter contact details including:
    - Mobile phone number
    - Email
    - Address
    - Registration number

- **Search Functionality**
  - Search for contacts by their registration number.

## Technologies

- **Flask**: A lightweight WSGI web application framework for Python.
- **MongoDB**: NoSQL database used for storing user and contact details.
- **PyMongo**: MongoDB driver for Python.
- (Optional) **Flask-Mail** or similar extension: For sending password reset emails.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/flask-mongo-contact-manager.git
   cd flask-mongo-contact-manager
   ```

2. **Create a virtual environment and activate it:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up MongoDB**

   Ensure you have MongoDB installed and running. Modify the MongoDB connection URL in the application configuration if necessary.

## Configuration

Create a configuration file or set environment variables for:

- `MONGO_URI`: Your MongoDB connection string.
- `SECRET_KEY`: A secret key for the Flask application.
- Email configuration settings if using Flask-Mail for password resets.

For example, you could create a `.env` file with:

```bash
MONGO_URI=mongodb://localhost:27017/yourdbname
SECRET_KEY=your-secret-key
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USE_TLS=1
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-email-password
```

Load the environment variables in your Flask application using [python-dotenv](https://github.com/theskumar/python-dotenv).

## Running the Application

Run the Flask development server:

```bash
flask run
```

Access the application at: [http://localhost:5000](http://localhost:5000).

## Project Structure

```
flask-mongo-contact-manager/
├── app.py                  # Main Flask application
├── config.py               # Application configurations
├── requirements.txt        # Python dependencies
├── templates/              # HTML templates for the app
│   ├── login.html          # Login page
│   ├── reset_password.html # Password reset page
│   ├── contacts.html       # Contact details form and search page
├── static/                 # Static files (CSS, JavaScript, etc.)
└── README.md               # This file
```

## License

Distributed under the MIT License. See `LICENSE` for more information.
