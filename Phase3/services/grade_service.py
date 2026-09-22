from models.degree_program import DegreeProgram
from models.exam_result import ExamResult
from models.exam_type import ExamType
from models.module import Module

# Notenberechnung, Zieldurchschnitt setzen.
class GradeService:

    def __init__(self, degree_program: DegreeProgram):
        self.degree_program = degree_program

    def get_current_average(self) -> float:
        grades = []

        for semester in self.degree_program.semesters:
            for module in semester.modules:
                for exam_result in module.exam_results:
                    if exam_result.grade is not None:
                        grades.append(exam_result.grade)

        if not grades:
            return 0.0

        return sum(grades) / len(grades)

    # Ziel-Notendurchschnitt
    def get_target_average(self) -> float:
        return self.degree_program.target_average_grade

    # Ziel-Notendurchschnitt setzen
    def set_target_average(self, target_average: float):
        if target_average < 1.0 or target_average > 6.0:
            raise ValueError(
                "Der Ziel-Durchschnitt muss zwischen 1.0 und 6.0 liegen."
            )

        self.degree_program.target_average_grade = target_average

    # Prüfungsergebnis hinzufügen
    def add_exam_result(
        self,
        module: Module,
        exam_result: ExamResult
    ):
        self.validate_grade(exam_result.grade)
        module.exam_results.append(exam_result)

    # Prüfungsergebnis löschen
    def delete_exam_result(
            self,
            module: Module,
            exam_result: ExamResult
    ):
        module.exam_results.remove(exam_result)

    # Wurde der Ziel-Notendurchschnitt erreicht?
    def has_reached_target_average(self) -> bool:
        return self.get_current_average() <= self.degree_program.target_average_grade

    # Prüfungsergebnis aktualisieren
    def update_exam_result(
            self,
            exam_result: ExamResult,
            exam_type: ExamType,
            grade: float
    ):
        self.validate_grade(grade)

        exam_result.exam_type = exam_type
        exam_result.grade = grade

    # Note validieren (1-6)
    def validate_grade(self, grade: float):
        if grade is None:
            return

        if grade < 1.0 or grade > 6.0:
            raise ValueError(
                "Note muss zwischen 1.0 and 6.0 liegen."
            )
