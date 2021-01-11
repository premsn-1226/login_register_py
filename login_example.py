
from flask import Flask, render_template, url_for, request, session, redirect
from pymongo import MongoClient    
import bcrypt

app = Flask(__name__)

client = MongoClient("mongodb://127.0.0.1:27017/")   
db = client.usrers
logindata = db.logindata

@app.route('/user')
def index():
    if 'username' in session:
        username = session['username']
        return render_template('logout.html',username = username)

    return render_template('index.html')
@app.route('/')
def main():
    return render_template('main.html')
@app.route('/login', methods=['POST'])
def login():
    users = logindata
    login_user = users.find_one({'name' : request.form['username'],'password':request.form['pass']})

    if login_user:
        if (request.form['username'] == login_user['name'] and request.form['pass'] == login_user['password']):
            session['username'] = request.form['username']
            user = session['username']
            return redirect(url_for('index'))

    return 'Invalid username/password'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = logindata
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = request.form['pass']
            users.insert({'name' : request.form['username'], 'password' : hashpass,'MobileNumber': request.form['number'],'emailId': request.form['email']})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'username already exists!'

    return render_template('register.html')

@app.route('/login')
def logout():
    session.pop('logged_in', None)
    return render_template('index.html')

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)