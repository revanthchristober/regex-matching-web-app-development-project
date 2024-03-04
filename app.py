from flask import Flask, render_template, request, redirect, url_for, session
import re

app = Flask(__name__)
app.secret_key = 'any_secret_key'  # Replace with your actual secret key

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        regex_pattern = request.form.get('regex', '')
        test_string = request.form.get('test_string', '')
        matches = re.findall(regex_pattern, test_string)
        # Store the form data and results in the session
        session['regex'] = regex_pattern
        session['test_string'] = test_string
        session['matches'] = matches
        # Redirect to the results route
        return redirect(url_for('results'))
    return render_template('index.html')

@app.route('/validate_email', methods=['GET', 'POST'])
def validate_email():
    # if request.method == 'POST':
        email = request.form.get('email', '')
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        is_valid = re.match(pattern, email) is not None
        # Store the form data and result in the session
        session['email'] = email
        session['is_valid'] = is_valid
        # Redirect to the results route
        return render_template('validate_email.html', email=email, is_valid=is_valid)

@app.route('/results', methods=['GET', 'POST'])
def results():
    # Initialize variables to store form data and results
    regex_pattern = session.get('regex', '')
    test_string = session.get('test_string', '')
    matches = session.get('matches', [])

    # Determine which form was submitted and process accordingly
    if 'test_string' in session:
        # Process regex matching results
        return render_template('results.html', regex=regex_pattern, test_string=test_string, matches=matches)
    else:
        # No form was submitted, return to home or show an error message
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
