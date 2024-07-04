from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# Update with your actual database credentials
try:
    conn = psycopg2.connect(
        dbname="todo_list",
        user="postgres",
        password="postgres",  # Use the password you set
        host="localhost"
    )
except Exception as e:
    print(f"Error connecting to the database: {e}")

@app.route('/')
def index():
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks;')
        tasks = cursor.fetchall()
        cursor.close()
        return render_template('index.html', tasks=tasks)
    except Exception as e:
        return str(e)

@app.route('/add', methods=['POST'])
def add_task():
    try:
        task_name = request.form['task_name']
        task_description = request.form['task_description']
        task_due_date = request.form['task_due_date']
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (task_name, task_description, task_due_date) VALUES (%s, %s, %s)',
                       (task_name, task_description, task_due_date))
        conn.commit()
        cursor.close()
        return redirect(url_for('index'))
    except Exception as e:
        return str(e)

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    try:
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET task_completed = TRUE WHERE task_id = %s', (task_id,))
        conn.commit()
        cursor.close()
        return redirect(url_for('index'))
    except Exception as e:
        return str(e)

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    if request.method == 'POST':
        try:
            task_name = request.form['task_name']
            task_description = request.form['task_description']
            task_due_date = request.form['task_due_date']
            cursor = conn.cursor()
            cursor.execute('UPDATE tasks SET task_name = %s, task_description = %s, task_due_date = %s WHERE task_id = %s',
                           (task_name, task_description, task_due_date, task_id))
            conn.commit()
            cursor.close()
            return redirect(url_for('index'))
        except Exception as e:
            return str(e)
    else:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks WHERE task_id = %s', (task_id,))
            task = cursor.fetchone()
            cursor.close()
            return render_template('edit.html', task=task)
        except Exception as e:
            return str(e)

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE task_id = %s', (task_id,))
        conn.commit()
        cursor.close()
        return redirect(url_for('index'))
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)

