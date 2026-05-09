document.addEventListener('DOMContentLoaded', () => {
    // Only run if on dashboard
    const tasksContainer = document.getElementById('tasks-container');
    if (!tasksContainer) return;

    // Connect to WebSocket
    const socket = io();
    
    // Listen for updates on the specific user channel
    socket.on(`tasks_update_${currentUserId}`, function(data) {
        console.log("Real-time update received:", data);
        fetchTasks();
        fetchAnalytics();
    });

    const addTaskForm = document.getElementById('add-task-form');

    // Fetch Initial Tasks
    fetchTasks();

    // Handle Form Submit
    addTaskForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const title = document.getElementById('title').value;
        const description = document.getElementById('description').value;
        const priority = document.getElementById('priority').value;

        try {
            const res = await fetch('/api/tasks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ title, description, priority })
            });

            if (res.ok) {
                addTaskForm.reset();
                // We rely on websocket to fetch tasks, but we can also trigger manually
            }
        } catch (error) {
            console.error("Error adding task:", error);
        }
    });

    // Fetch Tasks function
    async function fetchTasks() {
        try {
            const res = await fetch('/api/tasks');
            const tasks = await res.json();
            renderTasks(tasks);
        } catch (error) {
            console.error("Error fetching tasks:", error);
            tasksContainer.innerHTML = '<div class="flash flash-error">Failed to load tasks.</div>';
        }
    }

    // Render Tasks
    function renderTasks(tasks) {
        if (tasks.length === 0) {
            tasksContainer.innerHTML = '<p>No tasks yet. Add one above! ✨</p>';
            return;
        }

        tasksContainer.innerHTML = '';
        
        tasks.forEach(task => {
            const isCompleted = task.status === 'Completed';
            
            const taskEl = document.createElement('div');
            taskEl.className = `task-item ${isCompleted ? 'completed' : ''}`;
            
            taskEl.innerHTML = `
                <div class="task-content">
                    <div class="task-title">${escapeHTML(task.title)}</div>
                    ${task.description ? `<div class="task-desc">${escapeHTML(task.description)}</div>` : ''}
                    <div class="task-meta">
                        <span class="badge ${task.priority.toLowerCase()}">${task.priority} Priority</span>
                        <span>Created: ${new Date(task.created_date).toLocaleDateString()}</span>
                    </div>
                </div>
                <div class="task-actions">
                    ${!isCompleted ? `
                        <button class="btn btn-sm btn-secondary" onclick="updateTaskStatus(${task.id}, 'Completed')">Done ✓</button>
                    ` : `
                        <button class="btn btn-sm" onclick="updateTaskStatus(${task.id}, 'Pending')">Undo</button>
                    `}
                    <button class="btn btn-sm btn-primary" onclick="deleteTask(${task.id})">Delete 🗑️</button>
                </div>
            `;
            
            tasksContainer.appendChild(taskEl);
        });
    }

    // Global functions for inline onclick handlers
    window.updateTaskStatus = async (id, status) => {
        try {
            await fetch(`/api/tasks/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ status })
            });
        } catch (error) {
            console.error("Error updating task:", error);
        }
    };

    window.deleteTask = async (id) => {
        if(!confirm("Are you sure you want to delete this task?")) return;
        try {
            await fetch(`/api/tasks/${id}`, {
                method: 'DELETE'
            });
        } catch (error) {
            console.error("Error deleting task:", error);
        }
    };

    // Helper to prevent XSS
    function escapeHTML(str) {
        return str.replace(/[&<>'"]/g, 
            tag => ({
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                "'": '&#39;',
                '"': '&quot;'
            }[tag])
        );
    }
    
    // Fetch Analytics dynamically
    async function fetchAnalytics() {
        try {
            const res = await fetch('/api/analytics');
            const data = await res.json();
            document.getElementById('stat-total').textContent = data.total;
            document.getElementById('stat-completed').textContent = data.completed;
            document.getElementById('stat-pending').textContent = data.pending;
            document.getElementById('stat-percent').textContent = data.completion_percentage + '%';
        } catch (error) {
            console.error("Error fetching analytics:", error);
        }
    }
});
