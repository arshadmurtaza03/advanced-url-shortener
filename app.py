from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import string
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey123' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#Database Models

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False) # storing plain text for simplicity as per level
    urls = db.relationship('Url', backref='owner', lazy=True)

class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_url = db.Column(db.String(10), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Helper Function
def generate_short_id(num_of_chars):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=num_of_chars))

#Routes

@app.route('/')
@login_required
def dashboard():
    # Only show URLs belonging to the current logged-in user
    user_urls = Url.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', urls=user_urls, host_url=request.host_url)

@app.route('/shorten', methods=['POST'])
@login_required
def shorten_url():
    original_url = request.form.get('url')
    
    if not original_url:
        flash('Please enter a URL.')
        return redirect(url_for('dashboard'))

    # Basic check to ensure http/https
    if not original_url.startswith(('http://', 'https://')):
        original_url = 'http://' + original_url

    # Generate Short ID
    short_code = generate_short_id(5)
    while Url.query.filter_by(short_url=short_code).first():
        short_code = generate_short_id(5)

    new_url = Url(original_url=original_url, short_url=short_code, owner=current_user)
    db.session.add(new_url)
    db.session.commit()
    
    flash('URL Shortened Successfully!')
    return redirect(url_for('dashboard'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Constraint 1: Check length (5-9 characters)
        if len(username) < 5 or len(username) > 9:
            flash('Username must be between 5 to 9 characters long.')
            return redirect(url_for('signup'))

        # Constraint 2: Check if username exists
        if User.query.filter_by(username=username).first():
            flash('This username already exists... Try another one.')
            return redirect(url_for('signup'))

        # Create user
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created! Please login.')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        # Simple password check (for this assignment level)
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/<short_code>')
def redirect_to_url(short_code):
    link = Url.query.filter_by(short_url=short_code).first_or_404()
    return redirect(link.original_url)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)