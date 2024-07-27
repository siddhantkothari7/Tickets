from flask import Flask, render_template

app = Flask(__name__)

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
def landing_page():
    return render_template('landing_page.html')


@app.route('/setup')
def form():
    return render_template('setup.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    country_code = request.form['country_code']
    mobile_number = request.form['mobile_number']
    event_link = request.form['event_link']
    target_price = request.form['target_price']
    
    # Here you can add code to handle the form data, like saving it to a database or processing it
    # For now, we'll just print it to the console for demonstration purposes
    print(f"Country Code: {country_code}")
    print(f"Mobile Number: {mobile_number}")
    print(f"Event Link: {event_link}")
    print(f"Target Price: {target_price}")
    
    return "Form submitted successfully!"

# main driver function
if __name__ == '__main__':
    app.run(debug=True)