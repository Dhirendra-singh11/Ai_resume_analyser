from flask import Flask, render_template, request,  redirect
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'key696969' 

# MySQL configurations
app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "appuser"
app.config["MYSQL_PASSWORD"] = "app_password"
app.config["MYSQL_DB"] = "ai_resume_analyser"

mysql = MySQL(app)

@app.route("/", methods=["GET", "POST"])
def auth():
    if request.method == "POST":
        
        if "nameR" in request.form:
            username = request.form.get("emailR")
            password = request.form.get("passwordR")
            hashed_pass = generate_password_hash(password)
            cur = mysql.connection.cursor()
            try:
                cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_pass))
                mysql.connection.commit()
                print("Account created successfully! Please log in.", "success")
            except Exception as e:
                print(f"Error creating account: {e}", "danger")
            finally:
                cur.close()
            return redirect("/")

        
        username = request.form.get("email")
        password = request.form.get("password")
        cur = mysql.connection.cursor()
        cur.execute("SELECT password FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        if user and check_password_hash(user[0], password):
            print("Logged in successfully")
            
        else:
            print("Login failed")
        return redirect("/")

    
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
