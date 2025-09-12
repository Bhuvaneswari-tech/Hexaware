from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# -------------------------------
# Database Models
# -------------------------------
class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    instructor = db.Column(db.String(100))
    fee = db.Column(db.Numeric(10, 2))

#pip install -r requirements.txt

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

class Enrollment(db.Model):
    __tablename__ = "enrollments"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"))
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
    progress = db.Column(db.Integer, default=0)

    student = db.relationship("Student", backref="enrollments")
    course = db.relationship("Course", backref="enrollments")

# -------------------------------
# API Routes
# -------------------------------

@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json()
    student = Student(name=data["name"], email=data["email"])
    db.session.add(student)
    db.session.commit()
    return jsonify({"message": "Student added", "id": student.id})


@app.route("/courses", methods=["POST"])
def add_course():
    data = request.get_json()
    course = Course(title=data["title"], instructor=data["instructor"], fee=data["fee"])
    db.session.add(course)
    db.session.commit()
    return jsonify({"message": "Course added", "id": course.id})


@app.route("/enrollments", methods=["POST"])
def enroll_student():
    data = request.get_json()
    enrollment = Enrollment(student_id=data["student_id"], course_id=data["course_id"], 
                            progress=0)
    db.session.add(enrollment)
    db.session.commit()
    return jsonify({"message": "Student enrolled", "id": enrollment.id})

@app.route("/students/<int:student_id>/enrollments", methods=["GET"])
def get_student_courses(student_id):
    enrollments = Enrollment.query.filter_by(student_id=student_id).all()
    courses = [
        {"course_id": e.course.id, "title": e.course.title, "progress": e.progress}
        for e in enrollments
    ]
    return jsonify(courses)

@app.route("/enrollments/<int:enrollment_id>", methods=["PUT"])
def update_progress(enrollment_id):
    data = request.get_json()
    enrollment = Enrollment.query.get(enrollment_id)
    if not enrollment:
        return jsonify({"error": "Enrollment not found"}), 404
    enrollment.progress = data["progress"]
    db.session.commit()
    return jsonify({"message": "Progress updated"})

@app.route("/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Course not found"}), 404
    db.session.delete(course)
    db.session.commit()
    return jsonify({"message": "Course deleted"})

@app.route("/enrollments/<int:enrollment_id>", methods=["DELETE"])
def unenroll_student(enrollment_id):
    enrollment = Enrollment.query.get(enrollment_id)
    if not enrollment:
        return jsonify({"error": "Enrollment not found"}), 404
    db.session.delete(enrollment)
    db.session.commit()
    return jsonify({"message": "Unenrolled successfully"})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables if not exist
    app.run(debug=True)
