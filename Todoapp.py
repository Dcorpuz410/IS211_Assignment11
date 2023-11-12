from flask import Flask, redirect, request
app = Flask(__name__)

class Task:
    def __init__(self, description, email, priority):
        self.description = description
        self.email = email
        self.priority = priority

tasks = [
    Task("Buy vitamins", "me@myemail.com", "Medium"),
    Task("Fix the light bulb", "you@youremail.com", "Low"),
    Task("Tell kids to clean the bathroom", "them@theiremail.com", "High")
]

@app.route('/', methods=['GET'])
def tasks_manager():

    html = "<table>"
    html += "<tr><th>Description</th><th>Email</th><th>Priority</th></tr>"
    for task in tasks:
        html += f"<tr><td>{task.description}</td><td>{task.email}</td><td>{task.priority}</td></tr>"
    html += "</table>"

    form = """
        <form action="/submit" method="post">
            <label for="task">Task:</label>
            <input type="text" id="task" name="task" required><br>

            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required><br>

            <label for="priority">Priority:</label>
            <select id="priority" name="priority">
                <option value="Low">Low</option>
                <option value="Medium">Medium</option>
                <option value="High">High</option>
            </select><br>

            <input type="submit" value="Add To Do Item">
        </form>

        <form action="/clear" method="post">
            <input type="submit" value="Clear">
        </form>

    """


    error = request.args.get('error')
    if error == 'invalid_email':
        form += "<p style='color: red;'>Invalid email address.</p>"
    elif error == 'invalid_priority':
        form += "<p style='color: red;'>Invalid priority level.</p>"

    return html + form

@app.route('/submit', methods=['POST'])
def submit():

    description = request.form['task']
    email = request.form['email']
    priority = request.form['priority']


    if not is_valid_email(email):
        return redirect('/?error=invalid_email')
    if priority not in ['Low', 'Medium', 'High']:
        return redirect('/?error=invalid_priority')


    task = Task(description, email, priority)
    tasks.append(task)


    return redirect('/')

def is_valid_email(email):

    import re
    pattern = r"[^@]+@[^@]+\.[^@]+"
    return re.match(pattern, email)

@app.route('/clear', methods=['POST'])
def clear():
    global tasks
    tasks = []
    return redirect('/')

if __name__ == '__main__':
    app.run()