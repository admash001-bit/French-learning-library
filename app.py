from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model for Feedback
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

# Create database tables automatically
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/library')
def library():
    username = request.args.get('username', 'Guest')
    return render_template('library.html', username=username)

# Route to show the Feedback form page
@app.route('/feedback')
def feedback_page():
    return render_template('feedback.html')

# Route to save feedback into the database when submitted
@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    
    new_feedback = Feedback(name=name, email=email, message=message)
    db.session.add(new_feedback)
    db.session.commit()
    
    # Redirect to the thank you page instead of the library
    return redirect(url_for('library' ,username=name))

# NEW: Thank you route
@app.route('/thank-you')
def thank_you_page():
    return render_template('thank_you.html')
# Route for category levels (A1 - C2)
@app.route('/levels/<category_name>')
def show_levels(category_name):
    username = request.args.get('username', 'Guest')
    return render_template('levels.html', category_name=category_name, username=username)
if __name__ == '__main__':
    app.run(debug=True)


