import os
import sys
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import plotly.figure_factory as ff
import plotly.io as pio
import plotly.express as px
from typing import List, Dict, Any, Optional

# 添加父目录到路径，这样我们可以导入原始的gantt.py
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

app = Flask(__name__)

# 定义默认任务
DEFAULT_TASKS = [
    dict(Task="Reporting", Start='2025-05-01', Finish='2025-06-30', Resource='Reporting'),
    dict(Task="Evaluation and Testing", Start='2025-03-01', Finish='2025-04-30', Resource='Evaluation and Testing'),
    dict(Task="Model Optimization", Start='2024-11-01', Finish='2025-02-28', Resource='Model Optimization'),
    dict(Task="Baseline Models", Start='2024-05-01', Finish='2024-10-31', Resource='Baseline Models'),
    dict(Task="Data Preparation", Start='2024-01-01', Finish='2024-04-30', Resource='Data Preparation'),
]

# 任务数据文件路径
TASKS_FILE = os.path.join(current_dir, 'static', 'tasks.json')

def load_tasks() -> List[Dict[str, str]]:
    """从文件加载任务数据，如果文件不存在则使用默认任务"""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    else:
        # 确保目录存在
        os.makedirs(os.path.dirname(TASKS_FILE), exist_ok=True)
        # 保存默认任务到文件
        save_tasks(DEFAULT_TASKS)
        return DEFAULT_TASKS

def save_tasks(tasks: List[Dict[str, str]]) -> None:
    """保存任务数据到文件"""
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

def generate_gantt_chart(tasks: List[Dict[str, str]], filename_prefix: str = "gantt_chart") -> str:
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
        title='Gantt Chart for Individual Project',
        xaxis_title='日期',
        height=800,
        width=1600,
        font=dict(size=20)
    )

    # 定义输出路径
    static_dir = os.path.join(current_dir, 'static')
    png_path = os.path.join(static_dir, f"{filename_prefix}.png")
    html_path = os.path.join(static_dir, f"{filename_prefix}.html")
    
    # 保存高分辨率图片到静态目录
    fig.write_image(png_path, scale=4, width=1600, height=800)
    fig.write_html(html_path)  # 保存交互式HTML
    
    return f"{filename_prefix}.html"

@app.route('/')
def index():
    """主页路由"""
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/tasks', methods=['GET', 'POST'])
def manage_tasks():
    """处理任务管理请求"""
    if request.method == 'POST':
        # 获取表单数据
        data = request.json
        tasks = data.get('tasks', []) if data else []
        
        # 保存任务数据
        save_tasks(tasks)
        
        # 生成新的甘特图
        html_file = generate_gantt_chart(tasks)
        
        return jsonify({'success': True, 'html_file': html_file})
    else:
        # 获取任务数据
        tasks = load_tasks()
        return jsonify({'tasks': tasks})

@app.route('/add_task', methods=['POST'])
def add_task():
    """添加新任务"""
    tasks = load_tasks()
    
    # 获取表单数据
    task_name = request.form.get('task_name', '')
    start_date = request.form.get('start_date', '')
    finish_date = request.form.get('finish_date', '')
    
    # 验证数据有效性
    if not task_name or not start_date or not finish_date:
        return redirect(url_for('index'))
    
    # 创建新任务
    new_task = {
        'Task': task_name,
        'Start': start_date,
        'Finish': finish_date,
        'Resource': task_name  # 使用任务名称作为资源
    }
    
    # 添加到任务列表
    tasks.append(new_task)
    
    # 保存任务
    save_tasks(tasks)
    
    # 生成新的甘特图
    generate_gantt_chart(tasks)
    
    return redirect(url_for('index'))

@app.route('/update_task', methods=['POST'])
def update_task():
    """更新任务"""
    tasks = load_tasks()
    
    # 获取表单数据并进行类型转换和验证
    task_index_str = request.form.get('task_index', '')
    if not task_index_str or not task_index_str.isdigit():
        return redirect(url_for('index'))
    
    task_index = int(task_index_str)
    if task_index < 0 or task_index >= len(tasks):
        return redirect(url_for('index'))
    
    task_name = request.form.get('task_name', '')
    start_date = request.form.get('start_date', '')
    finish_date = request.form.get('finish_date', '')
    
    # 验证数据有效性
    if not task_name or not start_date or not finish_date:
        return redirect(url_for('index'))
    
    # 更新任务
    tasks[task_index]['Task'] = task_name
    tasks[task_index]['Start'] = start_date
    tasks[task_index]['Finish'] = finish_date
    tasks[task_index]['Resource'] = task_name
    
    # 保存任务
    save_tasks(tasks)
    
    # 生成新的甘特图
    generate_gantt_chart(tasks)
    
    return redirect(url_for('index'))

@app.route('/delete_task', methods=['POST'])
def delete_task():
    """删除任务"""
    tasks = load_tasks()
    
    # 获取表单数据并进行类型转换和验证
    task_index_str = request.form.get('task_index', '')
    if not task_index_str or not task_index_str.isdigit():
        return redirect(url_for('index'))
    
    task_index = int(task_index_str)
    if task_index < 0 or task_index >= len(tasks):
        return redirect(url_for('index'))
    
    # 删除任务
    tasks.pop(task_index)
    
    # 保存任务
    save_tasks(tasks)
    
    # 生成新的甘特图
    generate_gantt_chart(tasks)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    # 首次启动时生成甘特图
    tasks = load_tasks()
    generate_gantt_chart(tasks)
    
    # 启动Flask应用
    app.run(debug=True, host='0.0.0.0', port=5000)
