from flask import Flask, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_default_secret_key')  # Use an environment-specific key.
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)


# Dummy user data with hashed password
dummy_user = {
    "username": "Hadeyeenkah",
    "password": generate_password_hash("1234"),  # Use hashed password
    "profile": {
        "email": "tboysammy@gmail.com",
        "name": "Samuel",
        "recent_activity": [
            "Logged in at 10:00 AM",
            "Viewed property: Downtown Apartment",
            "Liked a listing: Modern Office Space"
        ]
    }
}

# Dummy property data
properties = [
    {"id": 1, "title": "Luxury Villa", "location": "Los Angeles", "price": 1200000, "description": "4-bedroom villa with pool."},
    {"id": 2, "title": "Modern Apartment", "location": "New York", "price": 850000, "description": "2-bedroom apartment downtown."},
    {"id": 3, "title": "Beach House", "location": "Miami", "price": 950000, "description": "3-bedroom house near the beach."},
    {"id": 4, "title": "Suburban Home", "location": "Chicago", "price": 600000, "description": "3-bedroom home with a large yard."},
]

# Default route
@app.route('/')
def home():
    return redirect(url_for('index'))  # Redirect to login by default

@app.route('/listings')
def listings():
    # Return the listings page
    return render_template('listings.html')

@app.route('/index')
def index():
    # Render the index page
    return render_template('index.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        # Dummy authentication with password hashing
        if username == dummy_user["username"] and check_password_hash(dummy_user["password"], password):
            session['user'] = {
                "username": username,
                "name": dummy_user["profile"]["name"],
                "email": dummy_user["profile"]["email"]
            }
            flash('Login successful!', 'success')
            return redirect(url_for('listings'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html', title="Login")

@app.route('/register')
def register():
    if request.method == 'POST':
        # Process registration logic
        username = request.form['username']
        password = request.form['password']
        # Save the user to the database (this is a placeholder example)
        # db.add_user(username, password)

        # Redirect to the listings page after registration
        return redirect(url_for('listings'))

    # Render the register page for GET requests
    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in
    if 'username' in session and 'email' in session:
        user = {
            'name': session.get('username'),
            'email': session.get('email')
        }
        return render_template('dashboard.html,')
    else:
        flash("Please log in to access the dashboard.", "danger")
        return redirect(url_for('profile_settings'))
    
    

#@app.route('/dashboard')
#def dashboard():
#    if 'user' not in session:
#        flash('Please log in to access the dashboard.', 'danger')
#        return redirect(url_for('login'))

#    return render_template('dashboard.html')
#user=session['user'], recent_activity=dummy_user["profile"]["recent_activity"],title="Dashboard")


@app.route('/search', methods=['GET', 'POST'])
def search_properties():
    search_results = []
    if request.method == 'POST':
        keyword = request.form.get('keyword', '').strip().lower()
        location = request.form.get('location', '').strip().lower()
        try:
            min_price = int(request.form.get('min_price', 0))
            max_price = int(request.form.get('max_price', 9999999))
        except ValueError:
            flash('Please enter valid numeric values for price range.', 'danger')
            return redirect(url_for('search_properties'))

        # Filter properties based on search criteria
        search_results = [
            prop for prop in properties
            if (keyword in prop['title'].lower())
            and (location in prop['location'].lower())
            and (min_price <= prop['price'] <= max_price)
        ]

        if not search_results:
            flash('No properties found matching your criteria.', 'info')

    return render_template('search.html', results=search_results, title="Search Properties")


@app.route('/property/<int:property_id>')
def property_details(property_id):
    # Find the property by id
    property = next((p for p in properties if p['id'] == property_id), None)
    if property is None:
        flash('Property not found.', 'danger')
        return redirect(url_for('search_properties'))

    return render_template('property_details.html', property=property, title=property["title"])


@app.route('/contact_agent/<int:property_id>', methods=['GET', 'POST'])
def contact_agent(property_id):
    property = next((p for p in properties if p['id'] == property_id), None)
    if property is None:
        flash('Property not found.', 'danger')
        return redirect(url_for('search_properties'))

    if request.method == 'POST':
        # Handle contact form submission
        message = request.form.get('message', '').strip()
        if message:
            flash('Your message has been sent to the agent!', 'success')
        else:
            flash('Please enter a message before submitting.', 'warning')
        return redirect(url_for('property_details', property_id=property_id))

    return render_template('contact_agent.html', property=property, title="Contact Agent")


@app.route('/request_viewing/<int:property_id>', methods=['GET', 'POST'])
def request_viewing(property_id):
    property = next((p for p in properties if p['id'] == property_id), None)
    if property is None:
        flash('Property not found.', 'danger')
        return redirect(url_for('search_properties'))

    if request.method == 'POST':
        # Logic for handling viewing request
        date = request.form.get('date', '').strip()
        if date:
            flash('Viewing request has been sent! We will contact you soon.', 'success')
        else:
            flash('Please select a date before submitting.', 'warning')
        return redirect(url_for('booking_confirmation'))

    return render_template('request_viewing.html', property=property, title="Request Viewing")


@app.route('/booking_confirmation')
def booking_confirmation():
    return render_template('booking_confirmation.html', title="Booking Confirmation")


@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user', None)
        flash('You have been logged out.', 'success')
    else:
        flash('You were not logged in.', 'info')
    return redirect(url_for('login'))


@app.route('/profile_settings', methods=['GET', 'POST'])
def profile_settings():
    if 'user' not in session:
        flash('Please log in to access Profile Settings.', 'danger')
        return redirect(url_for('login'))

    # Handle profile settings logic (e.g., update user details)
    if request.method == 'POST':
        flash('Profile updated successfully!', 'success')

    return render_template('profile_settings.html', user=dummy_user["profile"], title="Profile Settings")




if __name__ == '__main__':
    app.run(debug=True)



    
