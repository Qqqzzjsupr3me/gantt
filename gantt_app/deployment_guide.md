# 甘特图任务管理应用

这是一个基于Flask的甘特图任务管理应用，允许您添加、删除任务并生成甘特图。

## 功能特点

- 添加新任务（任务名称、开始日期、结束日期、资源）
- 删除现有任务
- 自动生成甘特图
- 响应式设计，支持移动设备

## 安装依赖

确保您已安装以下Python包：

```bash
pip install flask plotly pandas
```

## 运行应用

1. 进入应用目录：
   ```bash
   cd /hpc2hdd/home/zqiu183/Public/UCMP6050/gantt_app
   ```

2. 启动应用：
   ```bash
   python app.py
   ```

3. 在浏览器中访问：
   ```
   http://localhost:5000
   ```

## 使用说明

1. 在表单中填写任务信息：
   - 任务名称
   - 开始日期
   - 结束日期
   - 资源（可选）

2. 点击"添加任务"按钮创建新任务

3. 在任务列表中查看所有任务

4. 点击任务卡片上的"删除"按钮可以删除任务

5. 甘特图会自动更新以反映当前的任务状态

## 数据存储

任务数据保存在 `data/tasks.json` 文件中。

## 注意事项

- 日期格式必须为 YYYY-MM-DD
- 确保所有必填字段都已填写
- 结束日期必须晚于开始日期