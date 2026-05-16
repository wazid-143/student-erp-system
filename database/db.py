import sqlite3

connection = sqlite3.connect("students.db")
cursor = connection.cursor()


# USERS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT,
    email TEXT,
    password TEXT,
    role TEXT
)
""")


# STUDENTS TABLE
# STUDENTS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    roll TEXT,
    course TEXT,
    photo TEXT
)
""")


# ATTENDANCE TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT,
    status TEXT,
    date TEXT
)
""")


# MARKS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS marks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT,
    subject TEXT,
    marks TEXT
)
""")


# FEES TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS fees(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT,
    amount TEXT,
    status TEXT
)
""")


# TIMETABLE TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS timetable(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    day TEXT,
    subject TEXT,
    time TEXT
)
""")


# NOTIFICATIONS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS notifications(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT
)
""")


# DEFAULT ADMIN
cursor.execute(
    "SELECT * FROM users WHERE email=?",
    ("admin123@gmail.com",)
)

admin = cursor.fetchone()

if not admin:

    from werkzeug.security import generate_password_hash

    hashed_password = generate_password_hash("admin123")

    cursor.execute(
        "INSERT INTO users(fullname, email, password, role) VALUES(?,?,?,?)",
        ("Admin", "admin123@gmail.com", hashed_password, "admin")
    )

connection.commit()
connection.close()

print("Database Created Successfully")