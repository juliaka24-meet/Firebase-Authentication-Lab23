from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase


config = {
  "apiKey": "AIzaSyB7gX49YikSHgKlxdpIL6PbOEINiCnQM-A",
  "authDomain": "fir-auth-5e967.firebaseapp.com",
  "projectId": "fir-auth-5e967",
  "storageBucket": "fir-auth-5e967.appspot.com",
  "messagingSenderId": "555009691382",
  "appId": "1:555009691382:web:2c40e396da9b75af40a6d7",
  "measurementId": "G-KJ8MFYD1JC",
  "databaseURL": ""
} 

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        
        try:
            login_session["user"] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            return render_template("signin.html")
            print("hi")

    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]

        try:
            login_session["user"] = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            return render_template("signup.html")
            print("hello")

    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


if __name__ == '__main__':
    app.run(debug=True)