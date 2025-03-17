import os
import sys
import json
import sqlite3
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import plotly.figure_factory as ff
import plotly.io as pio
import plotly.express as px
from typing import List, Dict, Any, Optional
import uuid

# 添加父目录到路径，这样我们可以导入原始的gantt.py
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev_key_' + str(uuid.uuid4()))

# 默认任务
DEFAULT_TASKS = [
    dict(Task="Reporting", Start='2025-05-01', Finish='2025-06-30', Resource='Reporting'),
    dict(Task="Evaluation and Testing", Start='2025-03-01', Finish='2025-04-30', Resource='Evaluation and Testing'),
    dict(Task="Model Optimization", Start='2024-11-01', Finish='2025-02-28', Resource='Model Optimization'),
    dict(Task="Baseline Models", Start='2024-05-01', Finish='2024-10-31', Resource='Baseline Models'),
    dict(Task="Data Preparation", Start='2024-01-01', Finish='2024-04-30', Resource='Data Preparation'),
]

# 数据库路径
DB_PATH = os.path.join(current_dir, 'gantt.db')

def init_db():
    """初始化数据库"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 创建用户表
    c.execute('''
    CREATE TABLE IF NOT EXISTS users
    (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, 
    created_at TEXT DEFAULT CURRENT_TIMESTAMP)
    ''')
    
    # 创建项目表
    c.execute('''
    CREATE TABLE IF NOT EXISTS projects
    (id INTEGER PRIMARY KEY, name TEXT, description TEXT, 
    created_by INTEGER, created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users (id))
    ''')
    
    # 创建任务表
    c.execute('''
    CREATE TABLE IF NOT EXISTS tasks
    (id INTEGER PRIMARY KEY, project_id INTEGER, task TEXT, 
    start_date TEXT, finish_date TEXT, resource TEXT,
    FOREIGN KEY (project_id) REFERENCES projects (id))
    ''')
    
    # 如果没有默认项目，创建一个
    c.execute('SELECT COUNT(*) FROM projects')
    if c.fetchone()[0] == 0:
        c.execute('INSERT INTO projects (name, description, created_by) VALUES (?, ?, ?)',
                 ('默认项目', '一个用于展示甘特图功能的示例项目', 1))
        project_id = c.lastrowid
        
        # 添加默认任务
        for task in DEFAULT_TASKS:
            c.execute('''
            INSERT INTO tasks (project_id, task, start_date, finish_date, resource)
            VALUES (?, ?, ?, ?, ?)
            ''', (project_id, task['Task'], task['Start'], task['Finish'], task['Resource']))
    
    conn.commit()
    conn.close()

def load_tasks(project_id=1):
    """从数据库加载指定项目的任务"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
    SELECT task, start_date, finish_date, resource 
    FROM tasks 
    WHERE project_id = ?
    ''', (project_id,))
    
    tasks = []
    for row in c.fetchall():
        tasks.append({
            'Task': row[0],
            'Start': row[1],
            'Finish': row[2],
            'Resource': row[3]
        })
    
    conn.close()
    return tasks

def save_task(project_id, task_name, start_date, finish_date):
    """保存新任务到数据库"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
    INSERT INTO tasks (project_id, task, start_date, finish_date, resource)
    VALUES (?, ?, ?, ?, ?)
    ''', (project_id, task_name, start_date, finish_date, task_name))
    conn.commit()
    conn.close()

def update_task(task_id, task_name, start_date, finish_date):
    """更新数据库中的任务"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
    UPDATE tasks
    SET task = ?, start_date = ?, finish_date = ?, resource = ?
    WHERE id = ?
    ''', (task_name, start_date, finish_date, task_name, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    """删除数据库中的任务"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

def get_task_id(project_id, index):
    """根据项目ID和索引获取任务ID"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
    SELECT id FROM tasks WHERE project_id = ? ORDER BY id
    ''', (project_id,))
    tasks = c.fetchall()
    conn.close()
    
    if index < 0 or index >= len(tasks):
        return None
    
    return tasks[index][0]

def get_projects():
    """获取所有项目"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, name, description FROM projects')
    projects = [{'id': row[0], 'name': row[1], 'description': row[2]} for row in c.fetchall()]
    conn.close()
    return projects

def create_project(name, description, user_id):
    """创建新项目"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
    INSERT INTO projects (name, description, created_by)
    VALUES (?, ?, ?)
    ''', (name, description, user_id))
    project_id = c.lastrowid
    conn.commit()
    conn.close()
    return project_id

def generate_gantt_chart(tasks, project_id, filename_prefix="gantt_chart"):
    """生成甘特图并保存为图片和HTML"""
    # 获取所有唯一的资源值
    unique_resources = list(set(task['Resource'] for task in tasks))
    
    # 生成足够多的颜色 - 使用plotly express的颜色序列
    colors = px.colors.qualitative.Plotly[:len(unique_resources)] if len(unique_resources) <= 10 else [
        px.colors.qualitative.Plotly[i % 10] for i in range(len(unique_resources))
    ]
    
    # 创建甘特图
    fig = ff.create_gantt(tasks,
                         colors=colors,
                         index_col='Resource',
                         show_colorbar=True,
                         group_tasks=True,
                         showgrid_x=True,
                         showgrid_y=True)

    # 更新布局
    fig.update_layout(
        title='Gantt Chart for Project',
        xaxis_title='日期',
        height=800,
        width=1600,
        font=dict(size=20)
    )

    # 定义输出路径
    static_dir = os.path.join(current_dir, 'static')
    os.makedirs(static_dir, exist_ok=True)
    
    # 创建项目特定的文件名
    project_prefix = f"{filename_prefix}_{project_id}"
    png_path = os.path.join(static_dir, f"{project_prefix}.png")
    html_path = os.path.join(static_dir, f"{project_prefix}.html")
    
    # 保存高分辨率图片到静态目录
    fig.write_image(png_path, scale=4, width=1600, height=800)
    fig.write_html(html_path)  # 保存交互式HTML
    
    return f"{project_prefix}.html"

@app.route('/')
def index():
    """主页路由"""
    # 如果用户未登录，重定向到登录页面
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # 获取所有项目
    projects = get_projects()
    
    # 默认显示第一个项目
    project_id = request.args.get('project_id', '1')
    if not project_id.isdigit():
        project_id = '1'
    
    project_id = int(project_id)
    tasks = load_tasks(project_id)
    
    # 生成项目的甘特图
    chart_file = generate_gantt_chart(tasks, project_id)
    
    return render_template('multiuser_index.html', 
                          tasks=tasks, 
                          projects=projects, 
                          current_project=project_id,
                          chart_file=chart_file)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录"""
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT id, password FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()
        
        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('用户名或密码错误')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册"""
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        confirm = request.form.get('confirm', '')
        
        # 简单验证
        if not username or not password:
            flash('用户名和密码不能为空')
            return render_template('register.html')
        
        if password != confirm:
            flash('两次输入的密码不匹配')
            return render_template('register.html')
        
        # 检查用户名是否已存在
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT id FROM users WHERE username = ?', (username,))
        if c.fetchone():
            conn.close()
            flash('用户名已存在')
            return render_template('register.html')
        
        # 创建新用户
        hashed_password = generate_password_hash(password)
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                 (username, hashed_password))
        conn.commit()
        conn.close()
        
        flash('注册成功，请登录')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """用户退出"""
    session.clear()
    return redirect(url_for('login'))

@app.route('/projects/new', methods=['GET', 'POST'])
def new_project():
    """创建新项目"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form.get('name', '')
        description = request.form.get('description', '')
        
        if not name:
            flash('项目名称不能为空')
            return render_template('new_project.html')
        
        project_id = create_project(name, description, session['user_id'])
        return redirect(url_for('index', project_id=project_id))
    
    return render_template('new_project.html')

@app.route('/add_task', methods=['POST'])
def add_task():
    """添加新任务"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # 获取表单数据
    project_id = request.form.get('project_id', '1')
    if not project_id.isdigit():
        project_id = '1'
    
    project_id = int(project_id)
    task_name = request.form.get('task_name', '')
    start_date = request.form.get('start_date', '')
    finish_date = request.form.get('finish_date', '')
    
    # 验证数据有效性
    if not task_name or not start_date or not finish_date:
        flash('请填写完整任务信息')
        return redirect(url_for('index', project_id=project_id))
    
    # 添加任务到数据库
    save_task(project_id, task_name, start_date, finish_date)
    
    # 重新生成甘特图
    tasks = load_tasks(project_id)
    generate_gantt_chart(tasks, project_id)
    
    return redirect(url_for('index', project_id=project_id))

@app.route('/update_task', methods=['POST'])
def update_task_route():
    """更新任务"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # 获取表单数据
    project_id = request.form.get('project_id', '1')
    if not project_id.isdigit():
        project_id = '1'
    
    project_id = int(project_id)
    task_index = request.form.get('task_index', '')
    if not task_index.isdigit():
        flash('无效的任务索引')
        return redirect(url_for('index', project_id=project_id))
    
    task_index = int(task_index)
    task_id = get_task_id(project_id, task_index)
    if not task_id:
        flash('任务不存在')
        return redirect(url_for('index', project_id=project_id))
    
    task_name = request.form.get('task_name', '')
    start_date = request.form.get('start_date', '')
    finish_date = request.form.get('finish_date', '')
    
    # 验证数据有效性
    if not task_name or not start_date or not finish_date:
        flash('请填写完整任务信息')
        return redirect(url_for('index', project_id=project_id))
    
    # 更新任务
    update_task(task_id, task_name, start_date, finish_date)
    
    # 重新生成甘特图
    tasks = load_tasks(project_id)
    generate_gantt_chart(tasks, project_id)
    
    return redirect(url_for('index', project_id=project_id))

@app.route('/delete_task', methods=['POST'])
def delete_task_route():
    """删除任务"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # 获取表单数据
    project_id = request.form.get('project_id', '1')
    if not project_id.isdigit():
        project_id = '1'
    
    project_id = int(project_id)
    task_index = request.form.get('task_index', '')
    if not task_index.isdigit():
        flash('无效的任务索引')
        return redirect(url_for('index', project_id=project_id))
    
    task_index = int(task_index)
    task_id = get_task_id(project_id, task_index)
    if not task_id:
        flash('任务不存在')
        return redirect(url_for('index', project_id=project_id))
    
    # 删除任务
    delete_task(task_id)
    
    # 重新生成甘特图
    tasks = load_tasks(project_id)
    generate_gantt_chart(tasks, project_id)
    
    return redirect(url_for('index', project_id=project_id))

if __name__ == '__main__':
    # 初始化数据库
    init_db()
    
    # 为默认项目生成甘特图
    tasks = load_tasks()
    generate_gantt_chart(tasks, 1)
    
    # 启动Flask应用
    app.run(debug=True, host='0.0.0.0', port=5000)
