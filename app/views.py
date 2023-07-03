from flask import render_template, jsonify, request, Flask, make_response, send_file
from app import app, mysql
from flask_cors import CORS
import json
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
pdfmetrics.registerFont(TTFont('SimHei', 'simhei.ttf'))
CORS(app)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        raw_data = request.get_data(as_text=True)
        
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
        cursor = mysql.get_db().cursor()
        query = "DELETE FROM students WHERE student_id=%s"
        cursor.execute(query, (student_id,))
        mysql.get_db().commit()
        return jsonify({'message': 'Student deleted successfully'}), 200
    except Exception as e:
        print("An error occurred:", str(e))
        return jsonify({'error': 'An error occurred processing the request'}), 500

@app.route('/students', methods=['POST'])
def add_student():
    try:
        raw_data = request.get_data(as_text=True)
        data = json.loads(raw_data)
        cursor = mysql.get_db().cursor()
        query = """
            INSERT INTO students (student_id, name, class, major, college)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (data['student_id'], data['name'], data['class'], data['major'], data['college']))

        mysql.get_db().commit()

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

        cursor = mysql.get_db().cursor()

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

@app.route('/rewards_and_penalties/<string:student_id>/<string:reward_id>', methods=['PUT'])
def update_reward_and_penalty(student_id, reward_id):
    try:
        raw_data = request.get_data(as_text=True) 
        data = json.loads(raw_data)
        cursor = mysql.get_db().cursor()

        query = """
            UPDATE rewards_and_penalties
            SET reward_plan=%s
            WHERE student_id=%s AND reward_id=%s
        """
        cursor.execute(query, (data['reward_plan'], student_id, reward_id))
        mysql.get_db().commit()

        return jsonify({'message': 'Reward and Penalty information updated successfully'})
    except Exception as e:
        print("An error occurred:", str(e))
        return jsonify({'error': 'An error occurred processing the request'}), 500

@app.route('/rewards_and_penalties', methods=['POST'])
def add_reward_and_penalty():
    try:
        raw_data = request.get_data(as_text=True)
        data = json.loads(raw_data)
        cursor = mysql.get_db().cursor()
        query = """
            INSERT INTO rewards_and_penalties (student_id, name, class, major, college, reward_id, reward_name, reward_plan)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (data['student_id'], data['name'], data['class'], data['major'], data['college'], data['reward_id'], data['reward_name'], data['reward_plan']))
        mysql.get_db().commit()
        return jsonify({'message': 'Reward and penalty added successfully'})
    except Exception as e:
        print("An error occurred:", str(e))
        return jsonify({'error': 'An error occurred processing the request'}), 500

# 获取单个学生的信息
@app.route('/student_info', methods=['POST'])
def get_student_info():
    try:
        raw_data = request.get_data(as_text=True)
        data = json.loads(raw_data)
        cursor = mysql.get_db().cursor()
        query = "SELECT * FROM students WHERE student_id = %s"
        cursor.execute(query, (data['student_id'], ))
        student_info = cursor.fetchone()
        res = {
            'student_id': student_info[0],
            'name': student_info[1],
            'class': student_info[2],
            'major': student_info[3],
            'college': student_info[4]
        }
        return jsonify(res)
    except Exception as e:
        print("An error occurred:", str(e))
        return jsonify({'error': 'An error occurred processing the request'}), 500

...
@app.route('/check_student_id', methods=['POST'])
def check_student_id():
    try:
        raw_data = request.get_data(as_text=True)
        data = json.loads(raw_data)
        student_id = data.get('student_id')
        if student_id is None:
            raise ValueError("Missing student_id in request data")
        cursor = mysql.get_db().cursor()
        query = "SELECT COUNT(*) FROM students WHERE student_id = %s"
        cursor.execute(query, (student_id,))
        result = cursor.fetchone()
        exists = result[0] > 0
        return jsonify({'exists': exists})

    except Exception as e:
        print("An error occurred:", str(e))
        return jsonify({'error': 'An error occurred processing the request'}), 500

@app.route('/grades/export/<string:student_id>', methods=['GET'])
def export_grade_report(student_id):
    try:
        cursor = mysql.get_db().cursor()

        # Get student's name
        query = "SELECT name FROM students WHERE student_id = %s"
        cursor.execute(query, (student_id,))
        result = cursor.fetchone()
        if not result:
            return jsonify({'error': 'Student not found'})

        student_name = result[0]

        # Get grades
        query = "SELECT course, grade FROM grades WHERE student_id = %s"
        cursor.execute(query, (student_id,))
        result = cursor.fetchall()
        if not result:
            return jsonify({'message': 'No grades found for the student'})

        # Generate PDF report
        buffer = BytesIO()
        p = canvas.Canvas(buffer)

        # Set up report title and student name
        p.setFont('SimHei', 16)
        p.drawString(100, 700, '成绩单')
        p.setFont('SimHei', 12)
        p.drawString(100, 670, f'学号: {student_id}')
        p.drawString(100, 650, f'姓名: {student_name}')

        # Add grade information
        p.setFont('SimHei', 10)
        y = 600
        for row in result:
            course, grade = row
            p.drawString(100, y, f'课程: {course}')
            p.drawString(200, y, f'成绩: {grade}')
            y -= 20

        p.showPage()
        p.save()

        buffer.seek(0)

        # Return the PDF as a response
        response = make_response(buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=grade_report_{student_id}.pdf'
        return response

    except Exception as e:
        print("An error occurred:", str(e))
        return jsonify({'error': 'An error occurred processing the request'}), 500
    
@app.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    # 检查文件是否存在
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    # 如果用户没有选择文件，浏览器会提交一个没有文件的部分
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'success': 'Avatar uploaded successfully', 'file_path': os.path.join(app.config['UPLOAD_FOLDER'], filename)}), 200
    else:
        return jsonify({'error': 'Unsupported file type'}), 400