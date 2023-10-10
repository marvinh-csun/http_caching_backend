from flask import session,Blueprint, render_template, abort, request, flash, redirect, url_for
from datetime import datetime, timezone
from db import db
import jsonify
from sqlalchemy import text

task_blueprint = Blueprint('task_blueprint', __name__ , template_folder='templates')

def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

@task_blueprint.route("")
def index():
    statement = text(
            """
            SELECT * FROM task
            """
        )
    tasks = db.session.execute(statement,None)

    tasks = list(tasks)
    
    return render_template("task/index.html", tasks=tasks)

@task_blueprint.route("/update", methods=["POST"])
def update():
    if request.form.get("api_method") == "mark_completed":
        task_id = request.form.get("task_id")
        data = (
            {
            "task_id": task_id 
            }
        )
        statement = text(
            """
            UPDATE task
            SET
            completed_at = CURRENT_TIMESTAMP
            WHERE id = :task_id
            """
        )
        db.session.execute(statement,data)
        db.session.commit()
        session.pop('_flashes', None)
        flash(f'Task {task_id} completed')
        return redirect("/task")
    if request.form.get("api_method") == "mark_deleted":
        task_id = request.form.get("task_id")
        data = (
            {
            "task_id": task_id 
            }
        )
        statement = text(
            """
            UPDATE task
            SET
            deleted_at = CURRENT_TIMESTAMP
            WHERE id = :task_id
            """
        )
        db.session.execute(statement,data)
        db.session.commit()
        session.pop('_flashes', None)
        flash(f'Task {task_id} completed')
        return redirect("/task")


@task_blueprint.route("/<task_id>/edit", methods=["GET", "POST"])
def edit_task(task_id, methods=["GET", "POST"]):
    if request.method == "GET":
        print(task_id)
        data = (
            {
                "task_id": task_id
            }
        )
        statement = text(
            """
            SELECT * FROM task
            WHERE id=:task_id
            """
        )
        tasks = db.session.execute(statement,data)
        tasks = list(tasks)
        
        if len(tasks) == 0:
            return abort(404)
        else:
            return render_template("task/edit.html", task=tasks[0])
    elif request.method == "POST":
        due_date = request.form.get('due_date')
        task_name = request.form.get('task_name')
        task_description = request.form.get('task_description')

        data = (
            {
            "due_date": due_date,
            "task_name": task_name,
            "task_description": task_description,
            "task_id": task_id,
            }
        )
        statement = text(
            """
            UPDATE task 
            SET task_name=:task_name,task_description=:task_description, due_date=:due_date
            WHERE id=:task_id
            """
        )

        db.session.execute(statement,data)
        db.session.commit()
        
        session.pop('_flashes', None)
        flash('You sucessfully created a task')
        return redirect('/task')
    


        

@task_blueprint.route("/new", methods=["GET", "POST"])
def new_task():
    if request.method == "GET":
        
        min_utc_dt = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
        return render_template("task/new.html", min_date=min_utc_dt)
    elif request.method == "POST":
        due_date = request.form.get('due_date')
        task_name = request.form.get('task_name')
        task_description = request.form.get('task_description')
        data = (
            {
            "due_date": due_date,
            "task_name": task_name,
            "task_description": task_description
            }
        )
        statement = text(
            """
            INSERT INTO task (task_name, task_description, due_date)
            VALUES
            (:task_name, :task_description, :due_date)
            """
        )
        db.session.execute(statement,data)
        db.session.commit()
        
        session.pop('_flashes', None)
        flash('You sucessfully created a task')
        return redirect('/task')
        

