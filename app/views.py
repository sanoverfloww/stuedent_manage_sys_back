from flask import render_template, jsonify, request
from app import app, mysql
from flask_cors import CORS
import json

CORS(app)

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
            'student_id': row[0],
            'name': row[1],
            'class': row[2],
            'major': row[3],
            'college': row[4]
        }
        students.append(student)

    # Return the data as JSON (In a real-world app, you might render it into an HTML template)
    return jsonify(students)

@app.route('/students/<string:student_id>', methods=['PUT'])
def update_student(student_id):
    # print(f"PUT request received for student_id: {student_id}")
    try:
        # 获取请求的JSON数据
        raw_data = request.get_data(as_text=True)
        
        # 使用 json 模块解析 JSON 数据
        data = json.loads(raw_data)

        print(f"Parsed data is: {data}")
        # 创建一个光标来与MySQL互动
        cursor = mysql.get_db().cursor()

        # 执行SQL查询来更新学生信息
        query = """
            UPDATE students
            SET name=%s, class=%s, major=%s, college=%s
            WHERE student_id=%s
        """
        cursor.execute(query, (data['name'], data['class'], data['major'], data['college'], student_id))

        # 提交更改到数据库
        mysql.get_db().commit()

        # 返回一个简单的响应
        return jsonify({'message': 'Student updated successfully'})
    except Exception as e:
        print("An error occurred:", str(e))
        return jsonify({'error': 'An error occurred processing the request'}), 500

@app.route('/students/<string:student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        # 创建一个光标来与MySQL互动
        cursor = mysql.get_db().cursor()

        # 执行SQL查询来删除指定学生
        query = "DELETE FROM students WHERE student_id=%s"
        cursor.execute(query, (student_id,))

        # 提交更改到数据库
        mysql.get_db().commit()

        # 返回一个简单的响应
        return jsonify({'message': 'Student deleted successfully'}), 200
    except Exception as e:
        print("An error occurred:", str(e))
        return jsonify({'error': 'An error occurred processing the request'}), 500
