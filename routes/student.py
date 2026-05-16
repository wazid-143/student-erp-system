from flask import render_template, request, redirect, session, flash
import sqlite3
from werkzeug.utils import secure_filename
import os
from flask import jsonify

def register_student_routes(app):


    # ADD STUDENT
    @app.route('/add_student', methods=['GET', 'POST'])
    def add_student():

        if 'user' not in session:
            return redirect('/')

        if request.method == 'POST':

            name = request.form['name']
            email = request.form['email']
            roll = request.form['roll']
            course = request.form['course']

            photo = request.files['photo']

            filename = secure_filename(photo.filename)

            photo.save(os.path.join('static/uploads', filename))

            connection = sqlite3.connect("students.db")
            cursor = connection.cursor()
            email = request.form['email']
            cursor.execute(
            "INSERT INTO students(name, email, roll, course, photo) VALUES(?,?,?,?,?)",
            (name, email, roll, course, filename)

            )

            connection.commit()
            connection.close()

            flash("Student Added Successfully")

            return redirect('/view_students')

        return render_template("add_student.html")



    # VIEW STUDENTS
    @app.route('/view_students')
    def view_students():

        if 'user' not in session:
            return redirect('/')

        connection = sqlite3.connect("students.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM students")

        students = cursor.fetchall()

        connection.close()

        return render_template("view_students.html", students=students)



    # SEARCH STUDENT
    @app.route('/search_student', methods=['GET', 'POST'])
    def search_student():

        if 'user' not in session:
            return redirect('/')

        students = []

        if request.method == 'POST':

            search = request.form['search']

            connection = sqlite3.connect("students.db")
            cursor = connection.cursor()

            cursor.execute(
                "SELECT * FROM students WHERE name LIKE ?",
                ('%' + search + '%',)
            )

            students = cursor.fetchall()

            connection.close()

        return render_template("search_student.html", students=students)



    # DELETE STUDENT
    @app.route('/delete_student/<int:id>')
    def delete_student(id):

        if 'user' not in session:
            return redirect('/')

        connection = sqlite3.connect("students.db")
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM students WHERE id=?",
            (id,)
        )

        connection.commit()
        connection.close()

        flash("Student Deleted Successfully")

        return redirect('/view_students')



    # UPDATE STUDENT
    @app.route('/update_student/<int:id>', methods=['GET', 'POST'])
    def update_student(id):

        if 'user' not in session:
            return redirect('/')

        connection = sqlite3.connect("students.db")
        cursor = connection.cursor()

        if request.method == 'POST':

            name = request.form['name']
            roll = request.form['roll']
            course = request.form['course']

            photo = request.files['photo']

            filename = secure_filename(photo.filename)

            if filename != "":

                photo.save(os.path.join('static/uploads', filename))

            cursor.execute(
                "UPDATE students SET name=?, roll=?, course=?, photo=? WHERE id=?",
                (name, roll, course, filename, id)
            )

            connection.commit()
            connection.close()

            flash("Student Updated Successfully")

            return redirect('/view_students')

        cursor.execute(
            "SELECT * FROM students WHERE id=?",
            (id,)
        )

        student = cursor.fetchone()

        connection.close()

        return render_template("update_student.html", student=student)



    # ADD ATTENDANCE
    @app.route('/add_attendance', methods=['GET', 'POST'])
    def add_attendance():

        if 'user' not in session:
            return redirect('/')

        if request.method == 'POST':

            student_name = request.form['student_name']
            status = request.form['status']
            date = request.form['date']

            connection = sqlite3.connect("students.db")
            cursor = connection.cursor()

            cursor.execute(
                "INSERT INTO attendance(student_name, status, date) VALUES(?,?,?)",
                (student_name, status, date)
            )

            connection.commit()
            connection.close()

            flash("Attendance Added Successfully")

            return redirect('/view_attendance')

        return render_template("add_attendance.html")



    # VIEW ATTENDANCE
    @app.route('/view_attendance')
    def view_attendance():

        if 'user' not in session:
            return redirect('/')

        connection = sqlite3.connect("students.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM attendance")

        attendance = cursor.fetchall()

        connection.close()

        return render_template(
            "view_attendance.html",
            attendance=attendance
        )
    

    # ADD MARKS
    @app.route('/add_marks', methods=['GET', 'POST'])
    def add_marks():

        if 'user' not in session:
            return redirect('/')

        if request.method == 'POST':

            student_name = request.form['student_name']
            subject = request.form['subject']
            marks = request.form['marks']

            connection = sqlite3.connect("students.db")
            cursor = connection.cursor()

            cursor.execute(
                "INSERT INTO marks(student_name, subject, marks) VALUES(?,?,?)",
                (student_name, subject, marks)
            )

            connection.commit()
            connection.close()

            flash("Marks Added Successfully")

            return redirect('/view_marks')

        return render_template("add_marks.html")



    # VIEW MARKS
    @app.route('/view_marks')
    def view_marks():

        if 'user' not in session:
            return redirect('/')

        connection = sqlite3.connect("students.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM marks")

        marks = cursor.fetchall()

        connection.close()

        return render_template(
            "view_marks.html",
            marks=marks
        )
    

    # ADD FEES
    @app.route('/add_fees', methods=['GET', 'POST'])
    def add_fees():

        if 'user' not in session:
            return redirect('/')

        if request.method == 'POST':

            student_name = request.form['student_name']
            amount = request.form['amount']
            status = request.form['status']

            connection = sqlite3.connect("students.db")
            cursor = connection.cursor()

            cursor.execute(
                "INSERT INTO fees(student_name, amount, status) VALUES(?,?,?)",
                (student_name, amount, status)
            )

            connection.commit()
            connection.close()

            flash("Fees Added Successfully")

            return redirect('/view_fees')

        return render_template("add_fees.html")



    # VIEW FEES
    @app.route('/view_fees')
    def view_fees():

        if 'user' not in session:
            return redirect('/')

        connection = sqlite3.connect("students.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM fees")

        fees = cursor.fetchall()

        connection.close()

        return render_template(
            "view_fees.html",
            fees=fees
        )
    

    # STUDENT ATTENDANCE
    @app.route('/student_attendance')
    def student_attendance():

        if 'user' not in session:
            return redirect('/')

        connection = sqlite3.connect("students.db")
        cursor = connection.cursor()

        student_email = session['user']

        cursor.execute(
            "SELECT name FROM students WHERE email=?",
            (student_email,)
        )

        student_data = cursor.fetchone()

        student_name = student_data[0]

        cursor.execute(
            "SELECT * FROM attendance WHERE student_name=?",
            (student_name,)
        )

        attendance = cursor.fetchall()

        connection.close()

        return render_template(
            "student_attendance.html",
            attendance=attendance
        )


    # STUDENT MARKS
    @app.route('/student_marks')
    def student_marks():

        if 'user' not in session:
            return redirect('/')

        connection = sqlite3.connect("students.db")
        cursor = connection.cursor()

        student_email = session['user']

        cursor.execute(
            "SELECT name FROM students WHERE email=?",
            (student_email,)
        )

        student_data = cursor.fetchone()

        student_name = student_data[0]

        cursor.execute(
            "SELECT * FROM marks WHERE student_name=?",
            (student_name,)
        )

        marks = cursor.fetchall()

        connection.close()

        return render_template(
            "student_marks.html",
            marks=marks
        )

    # STUDENT FEES
    @app.route('/student_fees')
    def student_fees():

        if 'user' not in session:
            return redirect('/')

        connection = sqlite3.connect("students.db")
        cursor = connection.cursor()

        student_email = session['user']

        cursor.execute(
            "SELECT name FROM students WHERE email=?",
            (student_email,)
        )

        student_data = cursor.fetchone()

        student_name = student_data[0]

        cursor.execute(
            "SELECT * FROM fees WHERE student_name=?",
            (student_name,)
        )

        fees = cursor.fetchall()

        connection.close()

        return render_template(
            "student_fees.html",
            fees=fees
        )


     
    

    # STUDENT PROFILE
    @app.route('/student_profile')
    def student_profile():

        if 'user' not in session:
            return redirect('/')

        connection = sqlite3.connect("students.db")
        cursor = connection.cursor()

        student_email = session['user']

        cursor.execute(
            "SELECT * FROM students WHERE email=?",
            (student_email,)

        )

        student = cursor.fetchone()

        connection.close()

        return render_template(
            "student_profile.html",
            student=student
        )
    

    # STUDENT TIMETABLE
    @app.route('/student_timetable')
    def student_timetable():

        if 'user' not in session:
            return redirect('/')

        connection = sqlite3.connect("students.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM timetable")

        timetable = cursor.fetchall()

        connection.close()

        return render_template(
            "student_timetable.html",
            timetable=timetable
        )
    
    # ADD TIMETABLE
    @app.route('/add_timetable', methods=['GET', 'POST'])
    def add_timetable():

        if 'user' not in session:
            return redirect('/')

        if request.method == 'POST':

            day = request.form['day']
            subject = request.form['subject']
            time = request.form['time']

            connection = sqlite3.connect("students.db")
            cursor = connection.cursor()

            cursor.execute(
                "INSERT INTO timetable(day, subject, time) VALUES(?,?,?)",
                (day, subject, time)
            )

            connection.commit()
            connection.close()

            flash("Timetable Added Successfully")

            return redirect('/admin_dashboard')

        return render_template("add_timetable.html")
    

    # ADD NOTIFICATION
    @app.route('/add_notification', methods=['GET', 'POST'])
    def add_notification():

        if 'user' not in session:
            return redirect('/')

        if request.method == 'POST':

            message = request.form['message']

            connection = sqlite3.connect("students.db")
            cursor = connection.cursor()

            cursor.execute(
                "INSERT INTO notifications(message) VALUES(?)",
                (message,)
            )

            connection.commit()
            connection.close()

            flash("Notification Added Successfully")

            return redirect('/admin_dashboard')

        return render_template("add_notification.html")



    # VIEW NOTIFICATIONS
    @app.route('/view_notifications')
    def view_notifications():

        if 'user' not in session:
            return redirect('/')

        connection = sqlite3.connect("students.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM notifications")

        notifications = cursor.fetchall()

        connection.close()

        return render_template(
            "view_notifications.html",
            notifications=notifications
        )
    

    # STUDENTS API
    @app.route('/api/students')
    def api_students():

        connection = sqlite3.connect("students.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM students")

        students = cursor.fetchall()

        connection.close()

        data = []

        for student in students:

            data.append({

                "id": student[0],
                "name": student[1],
                "email": student[2],
                "roll": student[3],
                "course": student[4]

            })

        return jsonify(data)