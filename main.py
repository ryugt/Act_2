from server import app
from routes import auth, companies, companies_admin, users_admin

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    app.run(debug=True, use_reloader=False)
