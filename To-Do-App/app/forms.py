from datetime import datetime

# These are the only valid values for priority and category
PRIORITY_CHOICES = ['low', 'medium', 'high']

CATEGORY_CHOICES = [
    'General',
    'Work',
    'Personal',
    'Dev',
    'Health',
    'Finance',
    'Learning',
    'Shopping',
]

def validate_task_form(form_data):
    """
    Checks that the submitted form data is valid.
    Returns (cleaned_data, errors)
    - cleaned_data: a dict of safe, ready-to-save values
    - errors: a list of error messages (empty list = no errors)
    """
    errors = []
    cleaned = {}

    # Title
    title = form_data.get('title', '').strip()
    if not title:
        errors.append('Task title is required.')
    elif len(title) > 200:
        errors.append('Title must be 200 characters or fewer.')
    else:
        cleaned['title'] = title

    # Description
    description = form_data.get('description', '').strip()
    cleaned['description'] = description if description else None

    # Priority
    priority = form_data.get('priority', 'medium')
    if priority not in PRIORITY_CHOICES:
        priority = 'medium'   # Silently fix bad values
    cleaned['priority'] = priority

    # Category
    category = form_data.get('category', 'General').strip()
    if not category:
        category = 'General'
    cleaned['category'] = category

    # Due date
    due_date_str = form_data.get('due_date', '').strip()
    if due_date_str:
        try:
            # HTML date inputs 
            cleaned['due_date'] = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        except ValueError:
            errors.append('Invalid date format.')
            cleaned['due_date'] = None
    else:
        cleaned['due_date'] = None

    return cleaned, errors