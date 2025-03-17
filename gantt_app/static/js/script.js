document.addEventListener('DOMContentLoaded', function() {
    // 初始化日期选择器
    initDatePickers();
    
    // 初始化编辑任务按钮事件
    initEditTaskButtons();
    
    // 添加任务表单验证
    validateTaskForms();
});

/**
 * 初始化日期选择器
 */
function initDatePickers() {
    // 配置日期选择器
    const dateConfig = {
        dateFormat: "Y-m-d",
        locale: "zh",
        altInput: true,
        altFormat: "Y年m月d日",
        minDate: "2000-01-01",
        maxDate: "2030-12-31"
    };
    
    // 初始化所有日期选择器
    document.querySelectorAll('.date-picker').forEach(function(elem) {
        flatpickr(elem, dateConfig);
    });
}

/**
 * 初始化编辑任务按钮事件
 */
function initEditTaskButtons() {
    // 获取所有编辑按钮
    const editButtons = document.querySelectorAll('.edit-task-btn');
    
    // 为每个编辑按钮添加点击事件
    editButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            // 获取任务数据
            const index = this.dataset.index;
            const task = this.dataset.task;
            const start = this.dataset.start;
            const finish = this.dataset.finish;
            
            // 填充模态框表单
            document.getElementById('edit_task_index').value = index;
            document.getElementById('edit_task_name').value = task;
            document.getElementById('edit_start_date').value = start;
            document.getElementById('edit_finish_date').value = finish;
            
            // 重新初始化编辑表单中的日期选择器
            initEditDatePickers();
            
            // 显示模态框
            const modal = new bootstrap.Modal(document.getElementById('editTaskModal'));
            modal.show();
        });
    });
}

/**
 * 初始化编辑表单中的日期选择器
 */
function initEditDatePickers() {
    // 配置日期选择器
    const dateConfig = {
        dateFormat: "Y-m-d",
        locale: "zh",
        altInput: true,
        altFormat: "Y年m月d日",
        minDate: "2000-01-01",
        maxDate: "2030-12-31"
    };
    
    // 初始化编辑表单中的日期选择器
    flatpickr("#edit_start_date", dateConfig);
    flatpickr("#edit_finish_date", dateConfig);
}

/**
 * 表单验证
 */
function validateTaskForms() {
    // 添加任务表单验证
    const addForm = document.getElementById('add-task-form');
    if (addForm) {
        addForm.addEventListener('submit', function(event) {
            // 获取日期值
            const startDate = document.getElementById('start_date').value;
            const finishDate = document.getElementById('finish_date').value;
            
            // 验证结束日期是否晚于开始日期
            if (new Date(startDate) >= new Date(finishDate)) {
                event.preventDefault();
                alert('结束日期必须晚于开始日期！');
            }
        });
    }
    
    // 编辑任务表单验证
    const editForm = document.getElementById('edit-task-form');
    if (editForm) {
        editForm.addEventListener('submit', function(event) {
            // 获取日期值
            const startDate = document.getElementById('edit_start_date').value;
            const finishDate = document.getElementById('edit_finish_date').value;
            
            // 验证结束日期是否晚于开始日期
            if (new Date(startDate) >= new Date(finishDate)) {
                event.preventDefault();
                alert('结束日期必须晚于开始日期！');
            }
        });
    }
}

/**
 * 自动刷新甘特图
 */
function refreshGanttChart() {
    // 获取甘特图iframe
    const iframe = document.querySelector('.gantt-display iframe');
    
    // 刷新iframe
    if (iframe) {
        iframe.src = iframe.src;
    }
}
