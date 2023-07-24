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
  "databaseURL": "https://fir-auth-5e967-default-rtdb.firebaseio.com/"
} 

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

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

    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        name = request.form["name"]
        bio = request.form["bio"]

        try:
            login_session["user"] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {'name':name, 'bio':bio, 'email':email, 'password':password}
            db.child('Users').child(UID).set(user)
            return redirect(url_for('add_tweet'))
        except:
            return render_template("signup.html")

    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        title = request.form["title"]
        text = request.form["text"]

    try: 
        tweet = {'title':title,'text':text, 'uid':UID}
        db.child('Tweets').push(tweet)
    return render_template("add_tweet.html")


@app.route('/all_tweets', methods=['GET'])
def all_tweets():
    try: 
        tweets = db.child('Tweets').get().val()
        return redirect(url_for('all_tweets.html'), tweets=tweets)
    except:
        return render_template("add_tweet.html")

if __name__ == '__main__':
    app.run(debug=True)