
from peewee import *

db = SqliteDatabase('hw14.sqlite')


class BaseModel(Model):
    class Meta:
        database = db


class Task(BaseModel):
    id = AutoField()
    title = CharField()
    priority = CharField()
    category = CharField()

    class Meta:
        table_name = 'task'


class Log(BaseModel):
    id = AutoField()
    user = CharField()
    action = CharField()
    task = ForeignKeyField(Task, backref='logs')
    timestamp = CharField()
    status = CharField()

    class Meta:
        table_name = 'log'


db.connect()

db.drop_tables([Log, Task])
db.create_tables([Task, Log])

tasks_data = [
    {"id": 1, "title": "Fix auth bug", "priority": "High", "category": "Backend"},
    {"id": 2, "title": "Update UI", "priority": "Medium", "category": "Frontend"},
    {"id": 3, "title": "Database cleanup", "priority": "High", "category": "Database"},
    {"id": 4, "title": "Refactor code", "priority": "Low", "category": "Backend"},
    {"id": 5, "title": "Security patch", "priority": "High", "category": "Security"},
]

logs_data = [
    {"id": 1, "user": "admin", "action": "DELETE", "task": 3, "timestamp": "2024-05-01 10:00", "status": "OK"},
    {"id": 2, "user": "ivan",  "action": "UPDATE", "task": 2, "timestamp": "2024-05-01 10:05", "status": "FAIL"},
    {"id": 3, "user": "anna",  "action": "DELETE", "task": 1, "timestamp": "2024-05-01 10:07", "status": "OK"},
    {"id": 4, "user": "ivan",  "action": "DELETE", "task": 3, "timestamp": "2024-05-01 10:10", "status": "OK"},
    {"id": 5, "user": "admin", "action": "UPDATE", "task": 4, "timestamp": "2024-05-01 10:12", "status": "OK"},
    {"id": 6, "user": "anna",  "action": "UPDATE", "task": 2, "timestamp": "2024-05-01 10:15", "status": "OK"},
    {"id": 7, "user": "ivan",  "action": "DELETE", "task": 5, "timestamp": "2024-05-01 10:20", "status": "OK"},
]

Task.insert_many(tasks_data).execute()
Log.insert_many(logs_data).execute()

# query = (
#     Student
#     .select(
#         Student,
#         fn.COUNT(Enrollment.id).alias('course_count')
#     )
#     .join(Enrollment)
#     .group_by(Student)
#     .having(fn.COUNT(Enrollment.id) > 1)
# )

query = (Log.select(
    Log.user
    )
    .join(Task)
    .where(Log.action == 'DELETE')
    .order_by(Log.user.desc())
    .limit(1)

)

for record in query:
    print(record.user)

print("="*50)

query = (
    Task
    .select(Task.title)
    .join(Log)
    .where(Log.action == 'DELETE')
    .group_by(Task.id, Task.title)
    .having(fn.COUNT(Log.id) > 1)
)

for record in query:
    print(record.title)

print("="*50)

query = (Log.select(
    Log.user, fn.COUNT(Log.id).alias('fail_count')
    )
    .join(Task)
    .where((Log.status == 'FAIL') & (Task.category == 'Backend'))
    .order_by(fn.COUNT(Log.id).desc())
    .limit(1)

)
for record in query:
    print(record.user, record.fail_count)

print("="*50)

query = (Log.select(
    Log.user, Task.title, Log.timestamp
    )
    .join(Task)
    .where(Log.action == 'UPDATE')
    .order_by(Log.timestamp.desc())
    .limit(1)
)
for record in query:
    print(record.user, record.task.title, record.timestamp)

print("="*50)

query = (Log.select(
    Log.user, fn.COUNT().alias('cnt')
    )
    .join(Task)
    .where((Task.priority == 'High') & (Task.category == 'Security'))
    .group_by(Log.user)
)

for record in query:
    print(record.user, record.cnt)

print("="*50)
