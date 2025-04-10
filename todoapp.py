from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

todos = []

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>To Do List</title>
</head>
<body>
    <h1>To Do List</h1>

    {% if todos %}
    <table border="1">
        <tr>
            <th>Task</th>
            <th>Email</th>
            <th>Priority</th>
        </tr>
        {% for todo in todos %}
        <tr>
            <td>{{ todo.task }}</td>
            <td>{{ todo.email }}</td>
            <td>{{ todo.priority }}</td>
        </tr>
        {% endfor %}
    </table>
    {% else %}
    <p>No To Do items yet.</p>
    {% endif %}

    <h2>Add a New To Do Item</h2>
    <form action="/submit" method="post">
        <label for="task">Task:</label>
        <input type="text" id="task" name="task" required><br><br>

        <label for="email">Email:</label>
        <input type="email" id="email" name="email" required><br><br>

        <label for="priority">Priority:</label>
        <select id="priority" name="priority">
            <option value="Low">Low</option>
            <option value="Medium">Medium</option>
            <option value="High">High</option>
        </select><br><br>

        <input type="submit" value="Add To Do Item">
    </form>

    <h2>Clear All Items</h2>
    <form action="/clear" method="post">
        <input type="submit" value="Clear">
    </form>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, todos=todos)

@app.route('/submit', methods=['POST'])
def submit():
    task = request.form.get('task')
    email = request.form.get('email')
    priority = request.form.get('priority')

    if not task or not email or '@' not in email or priority not in ['Low', 'Medium', 'High']:
        return redirect('/')

    todos.append({'task': task, 'email': email, 'priority': priority})
    return redirect('/')

@app.route('/clear', methods=['POST'])
def clear():
    todos.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run()