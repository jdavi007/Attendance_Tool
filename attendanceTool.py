# Attendance Tool for CSC 4350 ith Dr. Hatch
# Jacob Davis, Pierre Djaroueh, Creed Warf


from flask import Flask, render_template, request, redirect, flash
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SeCrEtKeY'




# Connects to database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn




# Check-in
@app.route('/', methods=('GET', 'POST'))
def checkIn():
    conn = get_db_connection()
    students = conn.execute('SELECT id, firstName, lastName FROM students').fetchall() # get all students
    conn.close()

    if request.method == 'POST':
        selectedStudents = request.form.getlist('students')  # get selected student
        timestamp = datetime.now()  # current timestamp

        # add timestamp for check-in
        if selectedStudents:
            try:
                conn = get_db_connection()
                for student_id in selectedStudents:
                    conn.execute('INSERT INTO attendance (id, checkInTime) VALUES (?, ?)', (student_id, timestamp))
                conn.commit()
                conn.close()

                flash('Check-in successful!')
            except Exception:
                flash('Error: There was an issue checking you in.')

        return redirect('/')

    return render_template('checkin.html', students=students)




# Attendance
@app.route('/attendanceList', methods=('GET', 'POST'))
def attendanceList():
    conn = get_db_connection()
    students = conn.execute('SELECT id, firstName, lastName FROM students').fetchall()
    attendanceRecords = conn.execute('SELECT id, checkInTime FROM attendance').fetchall()
    conn.close()

    # dictionary to track check-ins
    attendanceDict = {student['id']: {'name': f"{student['firstName']} {student['lastName']}", 'checkins': []} for student in students}

    # add check-in times to dictionary
    for record in attendanceRecords:
        student_id = record['id']
        if student_id in attendanceDict:
            attendanceDict[student_id]['checkins'].append(record['checkInTime'])

    # create list for rendering
    attendanceList = []
    for data in attendanceDict.values():
        attendanceList.append
        ({
            'name': data['name'],
            'checkins': data['checkins']
        })

    return render_template('attendanceList.html', attendanceList=attendanceList)




# Hosting
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000, debug=True)