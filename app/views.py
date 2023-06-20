from flask import render_template, jsonify, request
from app import app, mysql

@app.route('/students')
def get_students():
    # Create a cursor to interact with MySQL
    cursor = mysql.get_db().cursor()
    
    # Execute SQL query to get all students
    cursor.execute("SELECT * FROM students")
    
    # Fetch all rows
    result = cursor.fetchall()
    students = []
    for row in result:
        student = {
            'id': row[0],
            'name': row[1],
            'class': row[2],
            'major': row[3],
            'college': row[4]
        }
        students.append(student)

    # Return the data as JSON (In a real-world app, you might render it into an HTML template)
    return jsonify(students)

@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    # 获取请求的JSON数据
    data = request.get_json()

    # 创建一个光标来与MySQL互动
    cursor = mysql.get_db().cursor()

    # 执行SQL查询来更新学生信息
    query = """
        UPDATE students
        SET name=%s, class=%s, major=%s, college=%s
        WHERE id=%s
    """
    cursor.execute(query, (data['name'], data['class'], data['major'], data['college'], student_id))

    # 提交更改到数据库
    mysql.get_db().commit()

    # 返回一个简单的响应
    return jsonify({'message': 'Student updated successfully'})