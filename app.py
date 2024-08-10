from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

def hashing(password):
    hash = ""
    specialChars = {
        "!":"1001",
        "@":"1011",
        "#":"1111",
        "$":"1002",
        "%":"1022",
        "^":"1222",
        "&":"2222",
        "*":"2003",
        "(":"2033",
        ")":"2333"
    }
    for i in range(len(password)):
        if password[i].isalpha():
            numbers = str(ord(password[i].lower()) - ord('a') + 1) + "@#" 
        elif password[i].isdigit():
            numbers = str(int(password[i]) * int(password[i]))
        else:
            numbers = specialChars[password[i]] + "#@"
        hash += numbers
    return hash

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///datas.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class data(db.Model):
    username = db.Column(db.String(20), primary_key = True)
    password = db.Column(db.String(80), nullable = False)

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/signup-content")
def loadSignUp():
    content = """<form action="/signup" method="post">
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
    return jsonify({'html': content})

@app.route("/signin-content")
def loadSignIn():
    signIn = """<div class="innerContainer">
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
    return jsonify({'html': signIn})

@app.route("/signup", methods=['POST'])
def signup():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    global hash

    user = data.query.filter_by(username=username).first()
    if user:
        return render_template('messages.html', message="Name Already exsit Login!", buttonMsg = "Login")

    if password == confirm_password:
        print(f"Username: {username}, Password: {password}, Confirm Password: {confirm_password}")

        hash = hashing(password)

        print(hash)
        datas = data(username = username, password = hash)
        db.session.add(datas)
        db.session.commit()
    else:
        return render_template('messages.html', message = "Try Again", buttonMsg = "Okay!")
    return render_template('messages.html', message = "Account Created Succesfully",buttonMsg="Try Again!")
    
@app.route("/signin", methods=['POST'])
def signin():
    username = request.form.get('username')
    password = request.form.get('password')

    user = data.query.filter_by(username = username).first()

    if user:
        print(user.password)
        print(hashing(password))
        if user.password == hashing(password):
                return render_template('messages.html', message = "Logged in SuccessFully", buttonMsg = "Okay!")     
    else:
        return render_template('messages.html', message = "Try Again", buttonMsg="Try Again!")



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
