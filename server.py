from flask import Flask

app = Flask(__name__)

app.secret_key = 'supersecretkey'
app.permanent_session_lifetime = 99999999

@app.route("/")
def home():
    return "¡La app Flask está funcionando en Render!"
