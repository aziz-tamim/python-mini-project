from app import db
from app.models import Task
from datetime import datetime, date, timedelta

# CREATE
def create_task(title, description=None, priority='medium',
                category='General', due_date=None):
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
def get_all_tasks(filter_by=None, sort_by='created_at',
                  category=None, search=None, due_filter=None):
    """
    Master query function — handles all combinations of
    filter, sort, category, search and due-date filtering.
    """
    query = Task.query

    # Search 
    if search:
        search_term = f'%{search}%'
        query = query.filter(
            db.or_(
                Task.title.ilike(search_term),
                Task.description.ilike(search_term)
            )
        )
    # Status filter
    if filter_by == 'active':
        query = query.filter_by(is_done=False)
    elif filter_by == 'completed':
        query = query.filter_by(is_done=True)

    # Category
    if category:
        query = query.filter_by(category=category)
    
    # Due date smart filter
    today = date.today()
    if due_filter == 'overdue':
        query = query.filter(
            Task.due_date < today,
            Task.is_done == False
        )
    elif due_filter == 'today':
        query = query.filter(
            Task.due_date == today,
            Task.is_done == False
        )
    elif due_filter == 'week':
        week_end = today + timedelta(days=7)
        query = query.filter(
            Task.due_date >= today,
            Task.due_date <= week_end,
            Task.is_done == False
        )
        
    # Apply sort
    if sort_by == 'due_date':
        query = query.order_by(
            Task.due_date.is_(None).asc(),
            Task.due_date.asc()
        )
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
    return Task.query.get_or_404(task_id)


def get_task_stats():
    """Progress bar stats."""
    total     = Task.query.count()
    completed = Task.query.filter_by(is_done=True).count()
    active    = total - completed
    percent   = round((completed / total) * 100) if total > 0 else 0
    return {
        'total': total, 'completed': completed,
        'active': active, 'percent': percent
    }

def get_sidebar_stats():
    """
    Everything the sidebar needs — counts per category,
    plus overdue/today/this-week counts.
    """
    today    = date.today()
    week_end = today + timedelta(days=7)

    # Due date group counts
    overdue_count = Task.query.filter(
        Task.due_date < today,
        Task.is_done == False
    ).count()

    today_count = Task.query.filter(
        Task.due_date == today,
        Task.is_done == False
    ).count()
    
    week_count = Task.query.filter(
        Task.due_date >= today,
        Task.due_date <= week_end,
        Task.is_done == False
    ).count()

    # Count tasks per category
    category_rows = db.session.query(
        Task.category,
        db.func.count(Task.id).label('count')
    ).filter(
        Task.is_done == False
    ).group_by(Task.category).all()
    
    categories = {row.category: row.count for row in category_rows}

    return {
        'overdue': overdue_count,
        'today':   today_count,
        'week':    week_count,
        'categories': categories
    }
    
def get_grouped_tasks(tasks):
    """
    Splits a flat list of tasks into groups by urgency.
    Used on the home page to show overdue tasks at the top.
    Returns an ordered list of (group_name, task_list) tuples.
    """
    today = date.today()
    groups = {
        'overdue': [],
        'today':   [],
        'upcoming':[],
        'no_date': []
    }

    for task in tasks:
        if task.is_done:
            groups['no_date'].append(task)
        elif task.due_date is None:
            groups['no_date'].append(task)
        elif task.due_date < today:
            groups['overdue'].append(task)
        elif task.due_date == today:
            groups['today'].append(task)
        else:
            groups['upcoming'].append(task)

    # Only return groups that actually have tasks
    result = []
    if groups['overdue']:
        result.append(('⚠️ Overdue', groups['overdue']))
    if groups['today']:
        result.append(('📅 Due Today', groups['today']))
    if groups['upcoming']:
        result.append(('📆 Upcoming', groups['upcoming']))
    if groups['no_date']:
        result.append(('📋 Tasks', groups['no_date']))

    return result

# UPDATE 

def update_task(task_id, title, description=None, priority='medium',
                category='General', due_date=None):
    task             = get_task_by_id(task_id)
    task.title       = title
    task.description = description
    task.priority    = priority
    task.category    = category
    task.due_date    = due_date
    db.session.commit()
    return task

def toggle_task_done(task_id):
    task         = get_task_by_id(task_id)
    task.is_done = not task.is_done
    db.session.commit()
    return task

# DELETE
def delete_task(task_id):
    task = get_task_by_id(task_id)
    db.session.delete(task)
    db.session.commit()
