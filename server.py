from flask import Flask
@app.route("/")
app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.permanent_session_lifetime = 99999999

