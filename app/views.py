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

@app.route('/students', methods=['POST'])
def add_student():
    try:
        # 获取请求的JSON数据
        raw_data = request.get_data(as_text=True)
        # 使用 json 模块解析 JSON 数据
        data = json.loads(raw_data)

        # 创建一个光标来与MySQL互动
        cursor = mysql.get_db().cursor()

        # 执行SQL查询来插入新的学生信息
        query = """
            INSERT INTO students (student_id, name, class, major, college)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (data['student_id'], data['name'], data['class'], data['major'], data['college']))

        # 提交更改到数据库
        mysql.get_db().commit()

        # 返回一个简单的响应
        return jsonify({'message': 'Student added successfully'})
    except Exception as e:
        print("An error occurred:", str(e))
        return jsonify({'error': 'An error occurred processing the request'}), 500

# 成绩列表
@app.route('/grades')
def get_grades():
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM grades")
    result = cursor.fetchall()
    grades = []
    for row in result:
        grade = {
            'student_id': row[0],
            'name': row[1],
            'course': row[2],
            'grade': row[3]
        }
        grades.append(grade)
    return jsonify(grades)

@app.route('/grades/<string:student_id>/<string:course>', methods=['DELETE'])
def delete_grade(student_id, course):
    try:
        cursor = mysql.get_db().cursor()
        query = "DELETE FROM grades WHERE student_id=%s AND course=%s"
        cursor.execute(query, (student_id, course))

        mysql.get_db().commit()

        return jsonify({'message': 'Grade deleted successfully'}), 200
    except Exception as e:
        print("An error occurred:", str(e))
        return jsonify({'error': 'An error occurred processing the request'}), 500


@app.route('/grades', methods=['POST'])
def add_grade():
    try:
        raw_data = request.get_data(as_text=True)
        data = json.loads(raw_data)
        cursor = mysql.get_db().cursor()
        query = """
            INSERT INTO grades (student_id, name, course, grade)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (data['student_id'], data['name'], data['course'], data['grade']))
        mysql.get_db().commit()
        return jsonify({'message': 'Grade added successfully'})
    except Exception as e:
        print("An error occurred:", str(e))
        return jsonify({'error': 'An error occurred processing the request'}), 500

@app.route('/grades/<string:student_id>/<string:course>', methods=['PUT'])
def update_grade(student_id, course):
    try:
        raw_data = request.get_data(as_text=True)
        
        data = json.loads(raw_data)

        # 创建一个光标来与MySQL互动
        cursor = mysql.get_db().cursor()

        # 执行SQL查询来更新成绩信息
        query = """
            UPDATE grades
            SET grade=%s
            WHERE student_id=%s AND course=%s
        """
        cursor.execute(query, (data['grade'], student_id, course))
        mysql.get_db().commit()

        return jsonify({'message': 'Grade updated successfully'})
    except Exception as e:
        print("An error occurred:", str(e))
        return jsonify({'error': 'An error occurred processing the request'}), 500
    
# 奖惩列表
@app.route('/rewards_and_penalties')
def get_rewards_and_penalties():
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM rewards_and_penalties")
    result = cursor.fetchall()
    res = []
    for row in result:
        temp = {
            'student_id': row[0],
            'name': row[1],
            'class': row[2],
            'major': row[3],
            'college': row[4],
            'reward_id': row[5],
            'reward_name': row[6],
            'reward_plan': row[7]
        }
        res.append(temp)
    return jsonify(res)

@app.route('/rewards_and_penalties/<string:reward_id>', methods=['DELETE'])
def delete_reward_and_penalty(reward_id):
    try:
        cursor = mysql.get_db().cursor()
        query = "DELETE FROM rewards_and_penalties WHERE reward_id=%s"
        cursor.execute(query, (reward_id,))

        mysql.get_db().commit()

        return jsonify({'message': 'Reward and penalty information deleted successfully'}), 200
    except Exception as e:
        print("An error occurred:", str(e))
        return jsonify({'error': 'An error occurred processing the request'}), 500
