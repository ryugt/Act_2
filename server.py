from flask import Flask

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.permanent_session_lifetime = 99999999

# 🔐 Corrección CWE-614:
app.config.update(
    SESSION_COOKIE_SECURE=True,     # Solo enviar cookies por HTTPS
    SESSION_COOKIE_HTTPONLY=True,   # No accesible por JavaScript
    SESSION_COOKIE_SAMESITE='Lax'   # Prevención básica contra CSRF
)