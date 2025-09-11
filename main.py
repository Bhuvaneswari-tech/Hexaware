from student import StudentDB

db = StudentDB()

# Add Students
db.add_student("John", 14, "9th", "john@example.com")
db.add_student("Charles", 16, "11th", "charles@example.com")

# List all students
db.list_students()

db.update_student("John", 21, "A+", "John_@example.com")

# Delete
db.delete_student("Charles")