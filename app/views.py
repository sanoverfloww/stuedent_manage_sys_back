from flask import render_template, jsonify
from app import app, mysql

@app.route('/students')
def get_students():
    # Create a cursor to interact with MySQL
    cursor = mysql.get_db().cursor()
    
    # Execute SQL query to get all students
    cursor.execute("SELECT * FROM students")
    
    # Fetch all rows
    students = cursor.fetchall()

    # Return the data as JSON (In a real-world app, you might render it into an HTML template)
    return jsonify(students)
