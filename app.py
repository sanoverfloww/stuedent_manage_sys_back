from flask import Flask

# 创建 Flask 应用实例
app = Flask(__name__)

# 一个简单的路由作为示例
@app.route('/')
def hello_world():
    return 'Hello, World!'

# 如果这个脚本是直接运行，那么启动 Flask 应用
if __name__ == '__main__':
    app.run()
