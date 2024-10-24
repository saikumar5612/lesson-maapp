from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:sai1234@localhost/school_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Secret key for session management
app.secret_key = '123'  # Change to a random secret key for session security

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define your models
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    lesson_url = db.Column(db.String(200), nullable=True)  # This will store the lesson URL

    def __repr__(self):
        return f'<Course {self.title}>'

# Dummy credentials for demonstration (you should replace this with a database check)
credentials = {
    "teacher": "password123"  # Example username and password
}

# Home route
@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', logged_in=True)  # Render home page if logged in
    return render_template('home.html', logged_in=False)  # Render home page if not logged in

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password are correct
        if username in credentials and credentials[username] == password:
            session['username'] = username  # Save the username in session
            flash('Login successful!', 'success')
            return redirect('/add_course')  # Redirect to Add Course page after successful login
        else:
            error = 'Invalid username or password!'
            return render_template('login.html', error=error)  # Render login page with error

    return render_template('login.html')  # Render the login page for GET request

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove the user from the session
    flash('You have been logged out!', 'info')
    return redirect('/')  # Redirect to home after logout

# Courses route
@app.route('/courses')
def courses():
    all_courses = Course.query.all()  # Fetch all courses from the database
    return render_template('courses.html', courses=all_courses,
                           logged_in='username' in session)  # Pass logged_in based on session
# Add Course route
@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if 'username' not in session:
        return redirect('/login')  # Redirect to login if not authenticated
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        lesson_url = request.form.get('lesson_url')  # Retrieve the lesson URL from the form
        new_course = Course(title=title, description=description, lesson_url=lesson_url)
        db.session.add(new_course)
        db.session.commit()
        return redirect('/courses')  # Redirect to courses after adding new course
    return render_template('add_course.html')  # Render the add course form

# Lesson Detail route
@app.route('/courses/<int:course_id>')
def lesson_detail(course_id):
    if 'username' not in session:
        return redirect('/login')  # Redirect to login if not authenticated
    course = Course.query.get_or_404(course_id)
    return render_template('lesson_detail.html', course=course)

# Route for Lesson 1 - Pick a Card Game
@app.route('/lesson1')
def lesson1():
    if 'username' not in session:
        return redirect('/login')  # Redirect to login if not authenticated
    return render_template('lesson1.html')

if __name__ == '__main__':
    app.run(debug=True)
