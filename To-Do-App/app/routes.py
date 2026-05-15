from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_utils import (
    get_all_tasks,
    get_task_stats,
    get_task_by_id,
    toggle_task_done,
    delete_task
)
main = Blueprint('main', __name__)

@main.route('/')
def index():
    filter_by = request.args.get('filter', None)
    sort_by   = request.args.get('sort', 'created_at')
    tasks = get_all_tasks(filter_by=filter_by, sort_by=sort_by)
    stats = get_task_stats()

    return render_template(
        'index.html',
        tasks=tasks,
        stats=stats,
        current_filter=filter_by,
        current_sort=sort_by
    )
    
# Toggle Task Done / not Done
@main.route('/task/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    task = toggle_task_done(task_id)
    flash(
        f'"{task.title}" marked as {"done ✓" if task.is_done else "active"}',
        'success'
    )
    return redirect(request.referrer or url_for('main.index'))

# DELETE TASK
@main.route('/task/<int:task_id>/delete', methods=['POST'])
def delete(task_id):
    task = get_task_by_id(task_id)
    title = task.title
    delete_task(task_id)
    flash(f'"{title}" was deleted.', 'success')
    return redirect(url_for('main.index'))

# ADD TASK
@main.route('/task/add', methods=['GET', 'POST'])
def add_task():
    return render_template('add_task.html')

# EDIT TASK
@main.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
    task = get_task_by_id(task_id)
    return render_template('edit_task.html', task=task)