from controllers.dashboard_controller import DashboardController
from models.student import Student
from models.degree_program import DegreeProgram
from models.semester import Semester
from models.module import Module
from models.exam_result import ExamResult
from models.exam_type import ExamType
from services.study_service import StudyService
from services.grade_service import GradeService

# Main Application.


# Degree Program
degree_program = DegreeProgram(
    name="Computer Science",
    current_semester=4
)

# Student
student = Student(
    student_number=123456,
    current_semester=4,
    degree_program=degree_program
)


# Semesters
semester_1 = Semester(name="Semester 1")
semester_2 = Semester(name="Semester 2")
semester_3 = Semester(name="Semester 3")
semester_4 = Semester(name="Semester 4")


# Modules
modulePython1 = Module(
    module_number="P001",
    name="Python Basics"
)

moduleSql = Module(
    module_number="SQL001",
    name="SQL Basics"
)

modulePython2 = Module(
    module_number="P002",
    name="Python Project: COurse Dashboard"
)


# Exam Results
result1 = ExamResult(
    exam_type=ExamType.PROJECT,
    grade=1.7
)

result2 = ExamResult(
    exam_type=ExamType.ONLINE_TEST,
    grade=2.0
)


# Relationships herstellen

student.degree_program = degree_program

degree_program.semesters.extend([
    semester_1,
    semester_2,
    semester_3,
    semester_4
])

semester_1.modules.append(modulePython1)
semester_2.modules.append(moduleSql)
semester_4.modules.append(modulePython2)

modulePython1.exam_results.append(result1)
moduleSql.exam_results.append(result2)


print(student)

# Test: StudyService

study_service = StudyService(degree_program)

print(f"Anzahl Module: {study_service.get_total_modules()} vs. abgeschlossene {study_service.get_completed_modules()}, Fortschritt: {study_service.get_study_progress()}")

# Test: GradeService

grade_service = GradeService(degree_program)

print(f"Notendurchschnitt: {grade_service.get_current_average():.2f}, Zieldurchschnitt: {grade_service.get_target_average():.2f}")

new_result = ExamResult(
    exam_type=ExamType.MANUSCRIPT,
    grade=1.3
)

grade_service.add_exam_result(
    moduleSql,
    new_result
)

print(f"Neuer Durchschnitt: {grade_service.get_current_average():.2f}")

controller = DashboardController(
    study_service,
    grade_service
)

new_result = ExamResult(
    exam_type=ExamType.MANUSCRIPT,
    grade=1.3
)

controller.on_exam_result_added(
    modulePython2,
    new_result
)

print(f"Module Python 2 ist abgeschlossen: {modulePython2.is_completed}, aktueller Durchschnitt: {grade_service.get_current_average()}")
