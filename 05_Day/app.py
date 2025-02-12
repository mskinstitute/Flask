from flask import Flask, request, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy  # pip install flask_sqlalchemy
import bcrypt  # pip install bcrypt
from flask_login import current_user

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret_key'

# Database setup
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(10), nullable=False)

    def __init__(self, first_name, last_name, gender, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.gender = gender
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))


# Create database tables
with app.app_context():
    db.create_all()


# Routes
@app.route('/')
@app.route('/home')
def home():
    print(current_user)
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            flash('Login successful!', 'success')
            return redirect('/home')
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('auth/login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        gender = request.form.get('gender')
        password = request.form.get('password')

        # Check if the email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please try again.', 'danger')
            return redirect('/login')

        try:
            new_user = User(first_name=first_name, last_name=last_name, email=email, gender=gender, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect('/login')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'danger')

    return render_template('auth/register.html')

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
