import pandas as pd
import numpy as np
from models import Task

def get_task_analytics(user_id):
    tasks = Task.query.filter_by(user_id=user_id).all()
    
    if not tasks:
        return {
            'total': 0,
            'completed': 0,
            'pending': 0,
            'completion_percentage': 0.0
        }
    
    # Convert tasks to list of dicts for pandas
    task_data = [{'status': t.status} for t in tasks]
    
    df = pd.DataFrame(task_data)
    
    total_tasks = len(df)
    
    # Using pandas and numpy for calculations
    status_counts = df['status'].value_counts()
    
    completed_tasks = int(status_counts.get('Completed', 0))
    pending_tasks = int(status_counts.get('Pending', 0))
    
    # Calculate percentage using numpy
    completion_percentage = float(np.round((completed_tasks / total_tasks) * 100, 1)) if total_tasks > 0 else 0.0
    
    return {
        'total': total_tasks,
        'completed': completed_tasks,
        'pending': pending_tasks,
        'completion_percentage': completion_percentage
    }
