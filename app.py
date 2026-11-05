from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Gayathri",
        database="student_db"
    )

@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        roll_no = request.form['roll_no']
        department = request.form['department']
        email = request.form['email']
        phone = request.form['phone']
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO students (name, roll_no, department, email, phone) VALUES (%s,%s,%s,%s,%s)",
                       (name, roll_no, department, email, phone))
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        name = request.form['name']
        roll_no = request.form['roll_no']
        department = request.form['department']
        email = request.form['email']
        phone = request.form['phone']
        cursor.execute("UPDATE students SET name=%s, roll_no=%s, department=%s, email=%s, phone=%s WHERE id=%s",
                       (name, roll_no, department, email, phone, id))
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for('index'))
    cursor.execute("SELECT * FROM students WHERE id=%s", (id,))
    student = cursor.fetchone()
    cursor.close()
    db.close()
    return render_template('edit.html', student=student)

@app.route('/delete/<int:id>')
def delete(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM students WHERE id=%s", (id,))
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)