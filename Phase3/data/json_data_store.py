import json

from models.degree_program import DegreeProgram
from models.exam_result import ExamResult
from models.exam_type import ExamType
from models.module import Module
from models.semester import Semester


class JsonDataStore:

    def __init__(self, file_path: str):
        self.file_path = file_path

    # Speichern als JSON-Daten
    def save(self, degree_program: DegreeProgram):
        data = {
            "degree_program": {
                "current_semester": degree_program.current_semester,
                "target_average_grade": degree_program.target_average_grade,
                "semesters": [
                    {
                        "name": semester.name,
                        "modules": [
                            {
                                "module_number": module.module_number,
                                "name": module.name,
                                "exam_results": [
                                    {
                                        "exam_type": exam_result.exam_type.value,
                                        "grade": exam_result.grade
                                    }
                                    for exam_result in module.exam_results
                                ]
                            }
                            for module in semester.modules
                        ]
                    }
                    for semester in degree_program.semesters
                ]
            }
        }

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

    # Laden der JSON-Daten
    def load(self) -> DegreeProgram:
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            raise

        degree_program_data = data["degree_program"]

        semesters = []

        for semester_data in degree_program_data["semesters"]:
            modules = []

            for module_data in semester_data["modules"]:
                exam_results = []

                for result_data in module_data["exam_results"]:
                    exam_result = ExamResult(
                        exam_type=ExamType(result_data["exam_type"]),
                        grade=result_data["grade"]
                    )

                    exam_results.append(exam_result)

                module = Module(
                    module_number=module_data["module_number"],
                    name=module_data["name"],
                    exam_results=exam_results
                )

                modules.append(module)

            semester = Semester(
                name=semester_data["name"],
                modules=modules
            )

            semesters.append(semester)

        return DegreeProgram(
            semesters=semesters,
            current_semester=degree_program_data["current_semester"],
            target_average_grade=degree_program_data["target_average_grade"]
        )