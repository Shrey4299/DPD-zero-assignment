# 🚀 API Documentation

## 🛠️ Framework

This project is built on Django, a high-level Python web framework. It provides a secure and scalable foundation for building web applications.

## 🗄️ Database Schema

The application uses a MySQL database named `Users` with two tables:

### Table: `Users`

This table stores user information.

- `id`: Integer, Primary Key, Auto Increment
- `username`: String(150), Unique, Not Null
- `email`: String(100), Unique, Not Null
- `password`: String(100), Not Null
- `full_name`: String(150), Not Null
- `age`: Integer
- `gender`: String(10), Not Null

### Table: `key_value_data`

This table stores key-value pairs.

- `id`: Integer, Primary Key, Auto Increment
- `key`: String(50), Unique, Not Null
- `value`: String(200), Not Null

## 🚀 Instructions to Run the Code

Before running the code, ensure that you have the following installed on your system:

- Python (3.x recommended)
- Django


## Installation
1. Install Python (version 3.7 or higher) on your system.
2. Clone this repository to your local machine:  git clone https://github.com/username/django-user-registration-api.git
3. Navigate to the project directory:  cd django-user-registration-API
4. Install the project dependencies: pip install -r requirements.txt
5. Apply the migrations to create the necessary database tables: python manage.py migrate
6. Start the Django development server: python manage.py runserver
7. The API will now be accessible at http://127.0.0.1:8000/.

Now you're ready to use the API! 🚀
