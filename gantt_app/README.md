# 甘特图任务管理应用

这是一个基于Flask的Web应用程序，用于管理项目任务并生成甘特图。

## 功能特点

- 添加、编辑和删除项目任务
- 自动更新甘特图
- 可视化项目时间线
- 导出甘特图为PNG和HTML格式

## 安装与运行

### 1. 安装依赖

首先，确保您的系统已安装Python 3.9或更高版本。然后安装所需依赖：

```bash
# 激活conda环境
conda activate base  # 或者您自己的环境

# 安装所需包
pip install flask plotly kaleido
```

### 2. 运行应用

```bash
# 进入应用目录
cd Public/UCMP6050/gantt_app

# 运行Flask应用
python app.py
```

应用将在 http://localhost:5000 启动。

## 使用指南

### 添加新任务

1. 在页面左侧的"添加新任务"表单中输入任务名称
2. 选择开始日期和结束日期
3. 点击"添加任务"按钮

### 编辑现有任务

1. 在任务列表中找到要编辑的任务
2. 点击任务卡片右下角的"编辑"按钮
3. 在弹出的对话框中修改任务详情
4. 点击"保存更改"按钮

### 删除任务

1. 在任务列表中找到要删除的任务
2. 点击任务卡片右下角的"删除"按钮

### 导出甘特图

- 在页面右侧的甘特图展示区下方，点击"下载PNG图片"按钮下载静态图片
- 点击"下载HTML文件"按钮下载交互式HTML版本的甘特图

## 技术栈

- 后端：Flask (Python)
- 前端：HTML, CSS, JavaScript
- 图表生成：Plotly
- 用户界面框架：Bootstrap 5
- 日期选择器：Flatpickr

## 文件结构

```
gantt_app/
├── app.py               # Flask应用主文件
├── static/
│   ├── css/
│   │   └── style.css    # 自定义样式
│   ├── js/
│   │   └── script.js    # 前端交互脚本
│   ├── gantt_chart.png  # 生成的甘特图图片
│   ├── gantt_chart.html # 生成的交互式甘特图
│   └── tasks.json       # 任务数据存储
└── templates/
    └── index.html       # 主页模板
```

## 注意事项

- 应用将自动从原始的gantt.py导入默认任务
- 您对任务的所有更改都会保存在tasks.json文件中
