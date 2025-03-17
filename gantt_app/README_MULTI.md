# 多用户甘特图协作平台

这是一个基于Flask的Web应用程序，专为团队协作设计，可以让多个用户共同管理项目任务并生成甘特图。

## 功能特点

- **多用户支持**：用户注册、登录和验证
- **多项目管理**：每个用户可以创建和参与多个项目
- **任务管理**：添加、编辑和删除项目任务
- **甘特图生成**：自动为每个项目生成甘特图
- **数据持久化**：使用SQLite数据库存储用户和项目数据
- **实时预览**：在浏览器中直接预览甘特图
- **导出功能**：支持将甘特图导出为PNG和HTML格式

## 安装与运行

### 1. 安装依赖

首先，确保您的系统已安装Python 3.9或更高版本。然后安装所需依赖：

```bash
# 激活conda环境
conda activate base  # 或者您自己的环境

# 安装所需包
pip install flask plotly kaleido werkzeug
```

### 2. 运行应用

```bash
# 进入应用目录
cd Public/UCMP6050/gantt_app

# 运行多用户版本的Flask应用
python multiuser_app.py
```

应用将在 http://localhost:5000 启动。

## 部署到网络

要将此应用部署到网络以便团队成员共同访问，请参考 `deployment_guide.md` 文件中的详细指南。有多种部署选项：

1. 使用PythonAnywhere（适合初学者）
2. 使用云服务器（如阿里云、腾讯云等）
3. 使用Docker容器化部署

## 使用指南

### 用户管理

1. **注册账户**：首次使用时，点击"立即注册"创建新账户
2. **登录系统**：使用您的用户名和密码登录

### 项目管理

1. **创建项目**：登录后，点击"创建项目"按钮
2. **切换项目**：在项目列表中点击要查看的项目

### 任务管理

1. **添加任务**：
   - 在"添加新任务"表单中输入任务名称
   - 选择开始日期和结束日期
   - 点击"添加任务"按钮

2. **编辑任务**：
   - 在任务列表中找到要编辑的任务
   - 点击任务卡片的"编辑"按钮
   - 在弹出的对话框中修改任务详情
   - 点击"保存更改"按钮

3. **删除任务**：
   - 在任务列表中找到要删除的任务
   - 点击任务卡片的"删除"按钮

### 导出甘特图

- 在页面右侧的甘特图展示区下方，点击"下载PNG图片"按钮下载静态图片
- 点击"下载HTML文件"按钮下载交互式HTML版本的甘特图

## 数据库结构

应用使用SQLite数据库存储数据，包含以下表：

1. **users**：存储用户信息
   - id: 用户ID
   - username: 用户名
   - password: 加密密码
   - created_at: 创建时间

2. **projects**：存储项目信息
   - id: 项目ID
   - name: 项目名称
   - description: 项目描述
   - created_by: 创建者ID
   - created_at: 创建时间

3. **tasks**：存储任务信息
   - id: 任务ID
   - project_id: 所属项目ID
   - task: 任务名称
   - start_date: 开始日期
   - finish_date: 结束日期
   - resource: 资源名称

## 技术栈

- **后端**：Flask (Python)
- **前端**：HTML, CSS, JavaScript
- **数据库**：SQLite
- **图表生成**：Plotly
- **用户界面**：Bootstrap 5
- **日期选择器**：Flatpickr
- **用户认证**：Werkzeug Security

## 文件结构

```
gantt_app/
├── multiuser_app.py        # 多用户版本主应用
├── app.py                  # 基础版本应用
├── gantt.db                # SQLite数据库
├── static/
│   ├── css/
│   │   └── style.css       # 自定义样式
│   ├── js/
│   │   └── script.js       # 前端交互脚本
│   ├── gantt_chart_1.png   # 项目1的甘特图图片
│   ├── gantt_chart_1.html  # 项目1的交互式甘特图
│   └── ...                 # 其他项目的甘特图
└── templates/
    ├── multiuser_index.html # 多用户版首页
    ├── login.html          # 登录页面
    ├── register.html       # 注册页面
    ├── new_project.html    # 创建项目页面
    └── index.html          # 基础版本首页
```

## 安全注意事项

- 部署到公共网络时，请确保配置HTTPS
- 生产环境中禁用Flask的debug模式
- 定期备份数据库
- 定期更新依赖以修复安全漏洞

## 未来功能计划

- 支持任务之间的依赖关系
- 添加任务进度跟踪
- 引入团队协作功能（任务分配）
- 添加任务提醒和通知
- 支持导出更多格式（例如PDF、Excel）
