from models.student import Student
from models.degree_program import DegreeProgram
from models.semester import Semester
from models.module import Module
from models.exam_result import ExamResult
from models.exam_type import ExamType

from services.study_service import StudyService
from services.grade_service import GradeService
from controllers.dashboard_controller import DashboardController


class Application:
    def __init__(self):
        self.student = None
        self.degree_program = None
        self.study_service = None
        self.grade_service = None
        self.dashboard_controller = None

    def start(self):
        self.initialize()

    def initialize(self):
        self.create_test_data()

        self.study_service = StudyService(self.degree_program)
        self.grade_service = GradeService(self.degree_program)

        self.dashboard_controller = DashboardController(
            self.study_service,
            self.grade_service
        )

    def create_test_data(self):
        # Degree Program
        self.degree_program = DegreeProgram(
            name="Computer Science",
            current_semester=4
        )

        # Student
        self.student = Student(
            student_number=123456,
            current_semester=4,
            degree_program=self.degree_program
        )

        # Semesters
        semester_1 = Semester(name="Semester 1")
        semester_2 = Semester(name="Semester 2")
        semester_3 = Semester(name="Semester 3")
        semester_4 = Semester(name="Semester 4")

        # Modules
        module_python1 = Module(
            module_number="P001",
            name="Python Basics"
        )

        module_sql = Module(
            module_number="SQL001",
            name="SQL Basics"
        )

        module_python2 = Module(
            module_number="P002",
            name="Python Project: Course Dashboard"
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

        self.student.degree_program = self.degree_program

        self.degree_program.semesters.extend([
            semester_1,
            semester_2,
            semester_3,
            semester_4
        ])

        semester_1.modules.append(module_python1)
        semester_2.modules.append(module_sql)
        semester_4.modules.append(module_python2)

        module_python1.exam_results.append(result1)
        module_sql.exam_results.append(result2)
