from flask import Flask
from flask_wtf import CSRFProtect
from datetime import timedelta
import os

app = Flask(__name__)

# CWE-259 – Usa variable de entorno o valor por defecto seguro
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'clave_dev_segura')

# Sesión limitada (mejor que 3 años)
app.permanent_session_lifetime = timedelta(days=1)

# Corrección CWE-614:
app.config.update(
    SESSION_COOKIE_SECURE=True,     # Solo enviar cookies por HTTPS
    SESSION_COOKIE_HTTPONLY=True,   # No accesible por JavaScript
    SESSION_COOKIE_SAMESITE='Lax'   # Prevención básica contra CSRF
)
# CWE-352 – Protección CSRF activada globalmente
csrf = CSRFProtect(app)