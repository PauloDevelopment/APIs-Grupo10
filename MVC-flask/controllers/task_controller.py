from flask import render_template, request, redirect, url_for
from models import db
from models.task import Task
from models.user import User

class TaskController:

    @staticmethod
    def list_tasks():
        tasks = Task.query.all()
        return render_template("tasks.html", tasks=tasks)

    @staticmethod
    def create_task():
        if request.method == "POST":
            
            title = request.form['title']
            description = request.form['description']
            user_id = int(request.form['user_id'])

            user_existente = db.session.query(User).filter_by(id=user_id).first()

            if not user_existente:
                return 'Usuário não encontrado!', 400

            new_task = Task(title=title, description=description, user_id=user_id)
            db.session.add(new_task)
            db.session.commit()

            return redirect(url_for("list_tasks"))

        users = User.query.all()
        return render_template("create_task.html", users=users)
    
    @staticmethod
    def update_task_status(task_id):
        task = db.session.query(Task).filter_by(id=task_id).first()

        if not task:
            return 'Tarefa não encontrada!', 400

        if task.status == 'Pendente':
            task.status = 'Concluído'
        else:
            task.status = 'Pendente'
        
        db.session.commit()

        return redirect(url_for("list_tasks"))

    @staticmethod
    def delete_task(task_id):
        task = db.session.query(Task).filter_by(id=task_id).first()

        if not task:
            return 'Tarefa não encontrada!', 400
        
        db.session.delete(task)
        db.session.commit()
    
        return redirect(url_for("list_tasks"))