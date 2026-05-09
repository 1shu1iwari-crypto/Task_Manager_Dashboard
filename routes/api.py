from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import Task
from extensions import db, socketio

api_bp = Blueprint('api', __name__)

def emit_tasks_update(user_id):
    # Emit an event to update the specific user's dashboard
    # We use a user-specific channel like "tasks_update_USER_ID"
    socketio.emit(f'tasks_update_{user_id}', {'message': 'Tasks updated'})

@api_bp.route('/tasks', methods=['GET'])
@login_required
def get_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_date.desc()).all()
    return jsonify([task.to_dict() for task in tasks])

from services.analytics import get_task_analytics

@api_bp.route('/analytics', methods=['GET'])
@login_required
def get_analytics():
    analytics = get_task_analytics(current_user.id)
    return jsonify(analytics)


@api_bp.route('/tasks', methods=['POST'])
@login_required
def add_task():
    data = request.json
    title = data.get('title')
    
    if not title:
        return jsonify({'error': 'Title is required'}), 400
        
    new_task = Task(
        title=title,
        description=data.get('description', ''),
        priority=data.get('priority', 'Medium'),
        status=data.get('status', 'Pending'),
        user_id=current_user.id
    )
    
    db.session.add(new_task)
    db.session.commit()
    
    emit_tasks_update(current_user.id)
    return jsonify(new_task.to_dict()), 201

@api_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
        
    data = request.json
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.priority = data.get('priority', task.priority)
    task.status = data.get('status', task.status)
    
    db.session.commit()
    emit_tasks_update(current_user.id)
    return jsonify(task.to_dict())

@api_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
        
    db.session.delete(task)
    db.session.commit()
    emit_tasks_update(current_user.id)
    return jsonify({'message': 'Task deleted'})
