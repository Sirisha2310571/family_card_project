import json
import os
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

USERS_FILE = 'users.json'
UPLOADS_DIR = 'static/uploads'

# Load or save users from JSON
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

# Initial user data
registered_users = load_users()
user_applied = {}

@app.route('/')
def home():
    if 'username' in session:
        return redirect('/dashboard')
    return redirect('/login')

# ---------------- Login ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect('/dashboard')
    if request.method == 'POST':
        uname = request.form['username']
        passwd = request.form['password']
        if uname in registered_users and registered_users[uname] == passwd:
            session['username'] = uname
            return redirect('/dashboard')
        else:
            return "Invalid credentials. <a href='/login'>Try again</a>"
    return render_template('login.html')

# ---------------- Register ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect('/dashboard')
    if request.method == 'POST':
        uname = request.form['username']
        passwd = request.form['password']
        if uname in registered_users:
            return "Username already exists. <a href='/register'>Try another</a>"
        registered_users[uname] = passwd
        save_users(registered_users)
        return redirect('/login')
    return render_template('register.html')

# ---------------- Dashboard ----------------
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/login')
    return render_template('dashboard.html', username=session['username'])

# ---------------- Apply for Family Card ----------------
@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':
        aadhaar = request.files['aadhaar']
        pan = request.files['pan']
        income = request.files['income']
        username = session['username']

        os.makedirs(UPLOADS_DIR, exist_ok=True)

        if aadhaar:
            aadhaar.save(os.path.join(UPLOADS_DIR, f"{username}_aadhaar.pdf"))
        if pan:
            pan.save(os.path.join(UPLOADS_DIR, f"{username}_pan.pdf"))
        if income:
            income.save(os.path.join(UPLOADS_DIR, f"{username}_income.pdf"))

        user_applied[username] = True
        return render_template('confirmation.html')

    return render_template('apply.html')

# ---------------- Other Pages (placeholders) ----------------
@app.route('/status')
def status():
    if 'username' not in session:
        return redirect('/login')
    return render_template('status.html')

@app.route('/stocks')
def stocks():
    if 'username' not in session:
        return redirect('/login')
    return render_template('stocks.html')

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect('/login')
    return render_template('profile.html')

@app.route('/contact')
def contact():
    if 'username' not in session:
        return redirect('/login')
    return render_template('contact.html')

# ---------------- Logout ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# ---------------- Run App ----------------
if __name__ == '__main__':
    app.run(debug=True)
