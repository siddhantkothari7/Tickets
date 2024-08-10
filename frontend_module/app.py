from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

# Configuration for SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'users.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the model for storing form data
class TrackingInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mobile_number = db.Column(db.String(12), nullable=False)
    event_link = db.Column(db.String(255), nullable=False)
    target_price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<TrackingInfo {self.id}>'

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
def landing_page():
    return render_template('landing_page.html')


@app.route('/setup')
def form():
    return render_template('form_input.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    country_code = request.form['country_code']
    mobile_number = request.form['mobile_number']
    event_link = request.form['event_link']
    target_price = request.form['target_price']
    
    # Save the form data to the database
    new_tracking_info = TrackingInfo(
        mobile_number=country_code + mobile_number,
        event_link=event_link,
        target_price=target_price
    )

    db.session.add(new_tracking_info)
    db.session.commit()
    
    return redirect(url_for('submit_success'))


@app.route('/submit_success')
def submit_success():
    return render_template('submit_success.html')

# main driver function
if __name__ == '__main__':
    #Create the database tables
    with app.app_context():
        db.create_all()
    app.run(debug=True)