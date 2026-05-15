from app import db
from datetime import datetime, date

class Task(db.Model):
    __tablename__ = 'tasks'

    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    priority    = db.Column(db.String(10), default='medium')
    category    = db.Column(db.String(50), default='General')
    due_date    = db.Column(db.Date, nullable=True)
    is_done     = db.Column(db.Boolean, default=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.id}: {self.title}>'

    @property
    def is_overdue(self):
        """Returns True if the task is past its due date and not done."""
        if self.due_date and not self.is_done:
            return self.due_date < date.today()
        return False

    @property
    def priority_order(self):
        """Converts priority to a number so we can sort by it."""
        return {'high': 1, 'medium': 2, 'low': 3}.get(self.priority, 2)