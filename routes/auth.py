from db import get_users_connection, hash_password
from flask import request, redirect, render_template, session, flash, url_for
from server import app
import bcrypt 

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect('/companies')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash("Usuario y contraseña obligatorios")
            return redirect(url_for('login'))
        if not username.isalnum():
            flash("Nombre de usuario no válido")
            return redirect(url_for('login'))
        conn = get_users_connection()
        #user = conn.execute("SELECT * FROM users WHERE username = '"+ username +"' AND password = '"+hash_password(password)+"'").fetchone()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?", 
            (username,)
        ).fetchone()
        conn.close()
        
        if user and bcrypt.checkpw(password.encode(), user['password'].encode()):
            session.permanent = True  # activa la duración definida en server.py
            session['username'] = user['username']
            session['role'] = user['role']
            session['company_id'] = user['company_id'] if 'company_id' in user.keys() else None
            return redirect('/companies')
        else:
            return render_template('auth/login.html', error="Invalid username or password")
    return render_template('auth/login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
