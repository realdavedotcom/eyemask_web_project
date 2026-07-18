from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""  # blank since you didn't set a password in XAMPP
app.config["MYSQL_DB"] = "student_db"

mysql = MySQL(app)

@app.route("/")
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    cur.close()
    return render_template("index.html", students=students)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO students(name,email,matric_number,department,faculty) VALUES(%s,%s,%s,%s,%s)",
            (
                request.form["name"],
                request.form["email"],
                request.form["matric_number"],
                request.form["department"],
                request.form["faculty"],
            ),
        )
        mysql.connection.commit()
        cur.close()
        return redirect("/")
    return render_template("add.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    cur = mysql.connection.cursor()
    if request.method == "POST":
        cur.execute(
            "UPDATE students SET name=%s,email=%s,matric_number=%s,department=%s,faculty=%s WHERE id=%s",
            (
                request.form["name"],
                request.form["email"],
                request.form["matric_number"],
                request.form["department"],
                request.form["faculty"],
                id,
            ),
        )
        mysql.connection.commit()
        cur.close()
        return redirect("/")
    cur.execute("SELECT * FROM students WHERE id=%s", (id,))
    student = cur.fetchone()
    cur.close()
    return render_template("edit.html", student=student)

@app.route("/delete/<int:id>")
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)