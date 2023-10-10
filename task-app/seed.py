from db import db
from sqlalchemy import text,Column, String, DateTime, dialects, Integer



def task_seeder():
    class Task(db.Model):
        __tablename__ = 'task'
        id = Column(Integer, primary_key=True)
        task_name = Column(String(255), nullable=False)
        task_description = Column(dialects.mysql.MEDIUMTEXT, nullable=False)
        due_date = Column(DateTime)
        completed_at = Column(DateTime)
        deleted_at = Column(DateTime)
        updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
        created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    data = []
    for i in range(15000,20000):
        data.append({
            "due_date": "2023-09-06 10:49:00",
            "task_name": "Random string Task "+str(i),
            "task_description":  "Random Description For Task "+str(i)
        })
    db.session.execute(db.insert(Task).values(data))
    db.session.commit()