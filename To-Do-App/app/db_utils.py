from app import db
from app.models import Task
from datetime import datetime

# CREATE
def create_task(title, description=None, priority='medium',
                category='General', due_date=None):
    """Add a new task to the database."""
    task = Task(
        title=title,
        description=description,
        priority=priority,
        category=category,
        due_date=due_date
    )
    db.session.add(task)
    db.session.commit()
    return task

# READ
def get_all_tasks(filter_by=None, sort_by='created_at'):
    """
    Get tasks from the database.
    filter_by: 'active', 'completed', or None (all)
    sort_by:   'due_date', 'priority', or 'created_at'
    """
    query = Task.query

    # Apply filter
    if filter_by == 'active':
        query = query.filter_by(is_done=False)
    elif filter_by == 'completed':
        query = query.filter_by(is_done=True)

    # Apply sort
    if sort_by == 'due_date':
        query = query.order_by(Task.due_date.asc())
    elif sort_by == 'priority':
        priority_order = db.case(
            (Task.priority == 'high',   1),
            (Task.priority == 'medium', 2),
            (Task.priority == 'low',    3),
            else_=2
        )
        query = query.order_by(priority_order)
    else:
        query = query.order_by(Task.created_at.desc())

    return query.all()


def get_task_by_id(task_id):
    """Get a single task. Returns 404 error automatically if not found."""
    return Task.query.get_or_404(task_id)


def get_task_stats():
    """Returns a summary dictionary used for the progress bar."""
    total     = Task.query.count()
    completed = Task.query.filter_by(is_done=True).count()
    active    = total - completed
    percent   = round((completed / total) * 100) if total > 0 else 0
    return {
        'total':     total,
        'completed': completed,
        'active':    active,
        'percent':   percent
    }


# UPDATE 

def update_task(task_id, title, description=None, priority='medium',
                category='General', due_date=None):
    """Update an existing task's details."""
    task = get_task_by_id(task_id)
    task.title       = title
    task.description = description
    task.priority    = priority
    task.category    = category
    task.due_date    = due_date
    db.session.commit()
    return task

def toggle_task_done(task_id):
    """Flip a task between done and not done."""
    task = get_task_by_id(task_id)
    task.is_done = not task.is_done
    db.session.commit()
    return task

# DELETE
def delete_task(task_id):
    """Permanently remove a task from the database."""
    task = get_task_by_id(task_id)
    db.session.delete(task)
    db.session.commit()
