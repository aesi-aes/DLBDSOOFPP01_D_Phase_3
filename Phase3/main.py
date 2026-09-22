import argparse

from application import Application
from data.config import DATA_FILE
from data.json_data_store import JsonDataStore
from models.degree_program import DegreeProgram
from models.exam_result import ExamResult
from models.exam_type import ExamType
from models.module import Module
from models.semester import Semester

def main():
    # Testdaten erstellen.
    def create_test_data():
        # Degree Program
        new_degree_program = DegreeProgram(
            current_semester=4,
            target_average_grade=2
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
        new_degree_program.semesters.extend([
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

        return new_degree_program

    # Commandline Parameter parsen: --demo startet Demo-Modus (ohne Laden/Speichern)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Startet die Anwendung mit Beispieldaten."
    )
    args = parser.parse_args()

    if args.demo:
        # Mit Testdaten speichern -> Speichern: aus
        degree_program = create_test_data()
        save_on_close = False
    else:
        # Daten aus JSON laden -> Speichern: an
        data_store = JsonDataStore(DATA_FILE)
        save_on_close = True

        try:
            degree_program = data_store.load()
        except FileNotFoundError:
            degree_program = DegreeProgram(
                name="Mein Studiengang"
            )

    # Application starten.
    application = Application(
        degree_program,
        save_on_close=save_on_close
    )

    application.start()


if __name__ == "__main__":
    main()

