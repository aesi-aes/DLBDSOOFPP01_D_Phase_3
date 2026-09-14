from models.student import Student
from models.degree_program import DegreeProgram

# Main Application.

student = Student(
    student_number=123456,
    current_semester=4
)

degree_program = DegreeProgram(
    name="Computer Science",
    current_semester=4
)

print(student)
print(degree_program)