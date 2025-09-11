import inspect
import student

def test_add_student_query():
    db = student.StudentDB()
    expected_query = "INSERT INTO students (name, age, grade, email) VALUES (%s, %s, %s, %s)"
    actual_query = inspect.getsource(db.add_student)
    assert expected_query in actual_query

def test_list_students_query():
    db = student.StudentDB()
    expected_query = "SELECT * FROM students"
    actual_query = inspect.getsource(db.list_students)
    assert expected_query in actual_query

def test_update_student_query():
    db = student.StudentDB()
    expected_query = "UPDATE students SET age = %s, grade = %s, email = %s WHERE name = %s"
    actual_query = inspect.getsource(db.update_student)
    assert expected_query in actual_query

def test_delete_student_query():
    db = student.StudentDB()
    expected_query = "DELETE FROM students WHERE name = %s"
    actual_query = inspect.getsource(db.delete_student)
    assert expected_query in actual_query

# --- Method signature tests ---

def test_add_student_signature():
    sig = inspect.signature(student.StudentDB.add_student)
    assert list(sig.parameters.keys()) == ["self", "name", "age", "grade", "email"]

def test_list_students_signature():
    sig = inspect.signature(student.StudentDB.list_students)
    assert list(sig.parameters.keys()) == ["self"]

def test_update_student_signature():
    sig = inspect.signature(student.StudentDB.update_student)
    assert list(sig.parameters.keys()) == ["self", "name", "age", "grade", "email"]

def test_delete_student_signature():
    sig = inspect.signature(student.StudentDB.delete_student)
    assert list(sig.parameters.keys()) == ["self", "name"]
