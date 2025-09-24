from flask import Flask, render_template, request,redirect,flash,session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from resume_analyser import handle_resume_analyser
import os
app = Flask(__name__)
app.secret_key = 'key696969'


app.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST", "127.0.0.1")
app.config["MYSQL_USER"] = os.environ.get("MYSQL_USER", "appuser")
app.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD", "app_password")
app.config["MYSQL_DB"] = os.environ.get("MYSQL_DB", "ai_resume_analyser")

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
                flash("Account created successfully! Please log in.", "success")
            except Exception as e:
                flash("This email is already registered. Please use another one.", "danger")
            finally:
                cur.close()
            return redirect("/")

        
        username = request.form.get("email")
        password = request.form.get("password")
        cur = mysql.connection.cursor()
        cur.execute("SELECT id,password FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        if not user:
            flash("User not found","danger")
            return redirect("/")
        user_id,has_pass=user
        if check_password_hash(has_pass, password):
            session["user_id"]=user_id
            flash("Logged in successfully","success")
            return render_template("main.html")
            
        else:
            flash("Login failed","danger")
        return redirect("/")

    
    return render_template("login.html")
@app.route("/main")
def main_pg():
    if "user_id" not in session:
        return redirect("/")
    return render_template("main.html")

@app.route("/upload",methods=["POST"])
def upload_file():
    if "user_id" not in session:
        return redirect("/")
    file=request.files["file"]
    if not file:
        flash("No file uploaded","error")
        return redirect("/main")
    
    try:
        ats_score,analyse_result=handle_resume_analyser(file,session["user_id"],mysql)
        return render_template("main.html", score=ats_score, result=analyse_result)
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/main")


if __name__ == "__main__":
    if not os.path.exists("upload_folder"):
        os.makedirs("upload_folder")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)
