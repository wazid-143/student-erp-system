from flask import render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3


def register_auth_routes(app):


    # LOGIN
    @app.route('/', methods=['GET', 'POST'])
    def login():

        if request.method == 'POST':

            email = request.form['email']
            password = request.form['password']

            connection = sqlite3.connect("students.db")
            cursor = connection.cursor()

            cursor.execute(
                "SELECT * FROM users WHERE email=?",
                (email,)
            )

            user = cursor.fetchone()

            connection.close()

            if user and check_password_hash(user[3], password):

                session['user'] = email
                session['role'] = user[4]

                if user[4] == "admin":

                    return redirect('/admin_dashboard')

                elif user[4] == "teacher":

                    return redirect('/teacher_dashboard')

                else:

                    return redirect('/student_dashboard')

            else:

                flash("Wrong Email or Password")

                return redirect('/')

        return render_template("login.html")



    # REGISTER
    @app.route('/register', methods=['GET', 'POST'])
    def register():

        if request.method == 'POST':

            fullname = request.form['fullname']
            email = request.form['email']
            password = request.form['password']

            role = "student"

            hashed_password = generate_password_hash(password)

            connection = sqlite3.connect("students.db")
            cursor = connection.cursor()

            cursor.execute(
                "INSERT INTO users(fullname, email, password, role) VALUES(?,?,?,?)",
                (fullname, email, hashed_password, role)
            )

            connection.commit()
            connection.close()

            flash("Registration Successful")

            return redirect('/')

        return render_template("register.html")



    # ADMIN DASHBOARD
    @app.route('/admin_dashboard')
    def admin_dashboard():

        if 'user' not in session:
            return redirect('/')

        if session['role'] != "admin":
            return "Access Denied"

        connection = sqlite3.connect("students.db")
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM students")
        total_students = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM attendance")
        total_attendance = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM marks")
        total_marks = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM fees")
        total_fees = cursor.fetchone()[0]

        connection.close()

        return render_template(
            "admin_dashboard.html",
            total_students=total_students,
            total_attendance=total_attendance,
            total_marks=total_marks,
            total_fees=total_fees
        )


    # TEACHER DASHBOARD
    @app.route('/teacher_dashboard')
    def teacher_dashboard():

        if 'user' not in session:
            return redirect('/')

        if session['role'] != "teacher":
            return "Access Denied"

        return render_template("teacher_dashboard.html")



    # STUDENT DASHBOARD
    @app.route('/student_dashboard')
    def student_dashboard():

        if 'user' not in session:
            return redirect('/')

        if session['role'] != "student":
            return "Access Denied"

        return render_template("student_dashboard.html")



    # CREATE USER
    @app.route('/create_user', methods=['GET', 'POST'])
    def create_user():

        if 'user' not in session:
            return redirect('/')

        if session['role'] != "admin":
            return "Access Denied"

        if request.method == 'POST':

            fullname = request.form['fullname']
            email = request.form['email']
            password = request.form['password']
            role = request.form['role']

            hashed_password = generate_password_hash(password)

            connection = sqlite3.connect("students.db")
            cursor = connection.cursor()

            cursor.execute(
                "INSERT INTO users(fullname, email, password, role) VALUES(?,?,?,?)",
                (fullname, email, hashed_password, role)
            )

            connection.commit()
            connection.close()

            flash("User Created Successfully")

            return redirect('/admin_dashboard')

        return render_template("create_user.html")
    

    # FORGOT PASSWORD
    @app.route('/forgot_password', methods=['GET', 'POST'])
    def forgot_password():

        if request.method == 'POST':

            email = request.form['email']
            new_password = request.form['new_password']

            hashed_password = generate_password_hash(new_password)

            connection = sqlite3.connect("students.db")
            cursor = connection.cursor()

            cursor.execute(
                "SELECT * FROM users WHERE email=?",
                (email,)
            )

            user = cursor.fetchone()

            if user:

                cursor.execute(
                    "UPDATE users SET password=? WHERE email=?",
                    (hashed_password, email)
                )

                connection.commit()
                connection.close()

                flash("Password Reset Successful")

                return redirect('/')

            else:

                flash("Email Not Found")

        return render_template("forgot_password.html")
    
    

    # LOGOUT
    @app.route('/logout')
    def logout():

        session.pop('user', None)
        session.pop('role', None)

        return redirect('/')