from models.degree_program import DegreeProgram
from models.exam_result import ExamResult
from models.module import Module

# Notenberechnung, Zieldurchschnitt setzen.
class GradeService:

    def __init__(self, degree_program: DegreeProgram):
        self.degree_program = degree_program
        self.target_average = 2.0

    def get_current_average(self) -> float:
        grades = []

        for semester in self.degree_program.semesters:
            for module in semester.modules:
                for exam_result in module.exam_results:
                    grades.append(exam_result.grade)

        if not grades:
            return 0.0

        return sum(grades) / len(grades)

    def get_target_average(self) -> float:
        return self.target_average

    def set_target_average(self, target_average: float):
        if target_average < 1.0 or target_average > 6.0:
            raise ValueError(
                "Der Ziel-Durchschnitt muss zwischen 1.0 und 6.0 liegen."
            )

        self.target_average = target_average

    def add_exam_result(
        self,
        module: Module,
        exam_result: ExamResult
    ):
        module.exam_results.append(exam_result)

    def has_reached_target_average(self) -> bool:
        return self.get_current_average() <= self.target_average

    