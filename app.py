from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    subject = db.Column(db.String(120), nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        subject = request.form.get('subject')
        grade = int(request.form.get('grade'))
        
        student = Student(name=name, subject=subject, grade=grade)
        db.session.add(student)
        db.session.commit()
    
    students = Student.query.all()
    return render_template('index.html', students=students)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)