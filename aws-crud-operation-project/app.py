from flask import Flask, render_template, request, redirect
import pymysql

app = Flask(__name__)

# RDS Database Connection
connection = pymysql.connect(
    host='YOUR_RDS_ENDPOINT',
    user='admin',
    password='YourPassword123',
    database='cruddb'
)

@app.route('/')
def index():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()
    return render_template('index.html', employees=rows)

@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        role = request.form['role']

        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO employees(name, email, role) VALUES(%s, %s, %s)",
            (name, email, role)
        )
        connection.commit()

        return redirect('/')

    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    cursor = connection.cursor()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        role = request.form['role']

        cursor.execute(
            "UPDATE employees SET name=%s, email=%s, role=%s WHERE id=%s",
            (name, email, role, id)
        )
        connection.commit()

        return redirect('/')

    cursor.execute("SELECT * FROM employees WHERE id=%s", (id,))
    employee = cursor.fetchone()

    return render_template('edit.html', employee=employee)

@app.route('/delete/<int:id>')
def delete_employee(id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM employees WHERE id=%s", (id,))
    connection.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)