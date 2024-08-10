from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Hashing function
def hashing(password):
    specialChars = {
        "!": "1001", "@": "1011", "#": "1111", "$": "1002",
        "%": "1022", "^": "1222", "&": "2222", "*": "2003",
        "(": "2033", ")": "2333"
    }
    hash = ""
    for char in password:
        if char.isalpha():
            hash += str(ord(char.lower()) - ord('a') + 1) + "@#"
        elif char.isdigit():
            hash += str(int(char) * int(char))
        else:
            hash += specialChars.get(char, "") + "#@"
    return hash

def signup():
    return """<form action="/signup" method="post">
    <div class="innerContainer">
        <div class="content">
            <label for="signup-username">Username</label><br/>
            <input type="text" class="inputs" id="signup-username" name="username" required>
        </div>
        <div class="content">
            <label for="signup-password">New Password:</label><br/>
            <input type="password" class="inputs" id="signup-password" name="password" required>
        </div>
        <div class="content">
            <label for="signup-confirm-password">Confirm Password:</label><br/>
            <input type="password" class="inputs" id="signup-confirm-password" name="confirm_password" required>
        </div>
        <div class="text-center content">
            <button class="button sign" type="submit">SignUp</button>
        </div>
        <p class="text-center content">Already Have an Account? <a onclick="loadSignIn()" class="links">Sign-In</a></p>
    </div>
    </form>"""

def signin():
    return """<div class="innerContainer">
        <form action="/signin" method="post">
            <div class="content">
                <label for="signin-username">Username:</label><br/>
                <input type="text" class="inputs" id="signin-username" name="username" required>
            </div>
            <div class="content">
                <label for="signin-password">Password:</label><br/>
                <input type="password" class="inputs" id="signin-password" name="password" required>
            </div>
            <div class="text-center content">
                <button class="button sign" type="submit">SignIn</button>
            </div>
            <p class="text-center content">Don't Have an Account? <a class="links" onclick="loadSignUp()">Sign-up</a></p>
        </form>
    </div>"""

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///datas.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Data(db.Model):
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(80), nullable=False)

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/signup-content")
def load_sign_up():
    return jsonify({'html': signup()})

@app.route("/signin-content")
def load_sign_in():
    return jsonify({'html': signin()})

@app.route("/signup", methods=['POST'])
def signup():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    user = Data.query.filter_by(username=username).first()

    if len(password) < 8:
        return render_template('messages.html', message="Provide a stronger password", buttonMsg="Let me Try Again!")
    if user:
        return render_template('messages.html', message="Name already exists. Login!", buttonMsg="Login")
    if password != confirm_password:
        return render_template('messages.html', message="Passwords do not match", buttonMsg="Try Again")

    hashed_password = hashing(password)
    new_user = Data(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    return render_template('messages.html', message="Account Created Successfully", buttonMsg="Login!")

@app.route("/signin", methods=['POST'])
def signin():
    username = request.form.get('username')
    password = request.form.get('password')

    user = Data.query.filter_by(username=username).first()

    if user and user.password == hashing(password):
        return render_template('messages.html', message="Logged in Successfully", buttonMsg="Okay!")
    
    return render_template('messages.html', message="Invalid credentials, try again.", buttonMsg="Try Again!")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')