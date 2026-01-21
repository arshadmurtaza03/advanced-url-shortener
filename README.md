# Advanced URL Shortener with Authentication 🔐

A full-stack URL Shortener web application built with Python and Flask. Unlike basic shorteners, this application features a complete User Authentication system, allowing users to sign up, log in, and manage their own private history of shortened links.

## 🚀 Key Features
- **User Authentication:** Secure Login and Signup functionality using `Flask-Login`.
- **Private History:** Users can only view and manage their own shortened URLs.
- **Custom Validation:**
  - Enforces username length constraints (5-9 characters).
  - Prevents duplicate username registration.
- **URL Management:**
  - Converts long URLs into unique 5-character short codes.
  - Automatically handles `http/https` protocols.
- **Responsive UI:** Clean, modern interface built with Bootstrap 5.

## 🛠️ Tech Stack
- **Backend:** Python, Flask
- **Database:** SQLite, SQLAlchemy
- **Authentication:** Flask-Login
- **Frontend:** HTML5, Bootstrap 5, Jinja2