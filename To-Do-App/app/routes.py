from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash
)
from app.db_utils import (
    get_all_tasks, get_task_stats, get_sidebar_stats,
    get_grouped_tasks, get_task_by_id,
    create_task, update_task,
    toggle_task_done, delete_task
)
from app.forms import validate_task_form, CATEGORY_CHOICES, PRIORITY_CHOICES

main = Blueprint('main', __name__)


# HOME PAGE 
@main.route('/')
def index():
    # Collect all URL parameters
    filter_by  = request.args.get('filter',     None)
    sort_by    = request.args.get('sort',        'created_at')
    category   = request.args.get('category',   None)
    search     = request.args.get('search',      '').strip()
    due_filter = request.args.get('due_filter',  None)

    tasks = get_all_tasks(
        filter_by=filter_by,
        sort_by=sort_by,
        category=category,
        search=search,
        due_filter=due_filter
    )

    use_groups = not search and not due_filter and not category and not filter_by
    if use_groups:
        grouped_tasks = get_grouped_tasks(tasks)
    else:
        grouped_tasks = None

    stats         = get_task_stats()
    sidebar_stats = get_sidebar_stats()

    return render_template(
        'index.html',
        tasks=tasks,
        grouped_tasks=grouped_tasks,
        stats=stats,
        sidebar_stats=sidebar_stats,
        current_filter=filter_by,
        current_sort=sort_by,
        current_category=category,
        current_search=search,
        current_due_filter=due_filter
    )


# ADD TASK
@main.route('/task/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'GET':
        return render_template(
            'add_task.html',
            categories=CATEGORY_CHOICES,
            priorities=PRIORITY_CHOICES,
            form_data={}
        )

    form_data = request.form
    cleaned, errors = validate_task_form(form_data)

    if errors:
        for error in errors:
            flash(error, 'error')
        return render_template(
            'add_task.html',
            categories=CATEGORY_CHOICES,
            priorities=PRIORITY_CHOICES,
            form_data=form_data
        )

    create_task(**cleaned)
    flash(f'"{cleaned["title"]}" added successfully!', 'success')
    return redirect(url_for('main.index'))


# EDIT TASK 
@main.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
    task = get_task_by_id(task_id)

    if request.method == 'GET':
        return render_template(
            'edit_task.html',
            task=task,
            categories=CATEGORY_CHOICES,
            priorities=PRIORITY_CHOICES,
            form_data={}
        )

    form_data = request.form
    cleaned, errors = validate_task_form(form_data)

    if errors:
        for error in errors:
            flash(error, 'error')
        return render_template(
            'edit_task.html',
            task=task,
            categories=CATEGORY_CHOICES,
            priorities=PRIORITY_CHOICES,
            form_data=form_data
        )

    update_task(task_id, **cleaned)
    flash(f'"{cleaned["title"]}" updated successfully!', 'success')
    return redirect(url_for('main.index'))


#  TOGGLE DONE 
@main.route('/task/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    task = toggle_task_done(task_id)
    flash(
        f'"{task.title}" marked as {"done ✓" if task.is_done else "active"}',
        'success'
    )
    return redirect(request.referrer or url_for('main.index'))


#  DELETE TASK 
@main.route('/task/<int:task_id>/delete', methods=['POST'])
def delete(task_id):
    task  = get_task_by_id(task_id)
    title = task.title
    delete_task(task_id)
    flash(f'"{title}" was deleted.', 'success')
    return redirect(url_for('main.index'))