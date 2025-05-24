from flask import Flask

app = Flask(__name__)

@app.route("/")
app.secret_key = 'supersecretkey'
app.permanent_session_lifetime = 99999999

