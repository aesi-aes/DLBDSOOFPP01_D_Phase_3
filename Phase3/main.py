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
            current_semester=3,
            target_average_grade=2
        )

        # Semesters
        semester_1 = Semester(name="Semester 1")
        semester_2 = Semester(name="Semester 2")
        semester_3 = Semester(name="Semester 3")
        semester_4 = Semester(name="Semester 4")

        # Modules
        module_python1 = Module(module_number="P001", name="Python Basics")
        module_python2 = Module(module_number="P002", name="Python Project: Course Dashboard")
        module_sql = Module(module_number="SQL001", name="SQL Basics")
        module_game_dev= Module(module_number="GD002", name="Game Development - Programmieren mit C#")
        module_game_art = Module(module_number="GD002", name="Game Art - 3D-Modellieren mit Blender")
        module_english = Module(module_number="E001", name="English in Software Development")
        module_german = Module(module_number="G001", name="Deutsch in der Softwareentwicklung")
        module_unity = Module(module_number="GD003", name="Erste Schritte mit der Unity-Engine")

        # Exam Results
        result1 = ExamResult(exam_type=ExamType.PROJECT, grade=1.7)
        result2 = ExamResult(exam_type=ExamType.ONLINE_TEST, grade=2.0)
        result3 = ExamResult(exam_type=ExamType.MANUSCRIPT, grade=2.2)
        result4 = ExamResult(exam_type=ExamType.ONLINE_TEST, grade=2.0)
        result5 = ExamResult(exam_type=ExamType.ONLINE_TEST, grade=None)
        result6 = ExamResult(exam_type=ExamType.PROJECT, grade=None)
        result7 = ExamResult(exam_type=ExamType.ONLINE_TEST, grade=1.5)
        result8 = ExamResult(exam_type=ExamType.PROJECT, grade=2)
        result9 = ExamResult(exam_type=ExamType.MANUSCRIPT, grade=3)
        result10 = ExamResult(exam_type=ExamType.PROJECT, grade=1)
        result11 = ExamResult(exam_type=ExamType.PROJECT, grade=None)

        # Relationships herstellen
        new_degree_program.semesters.extend([
            semester_1,
            semester_2,
            semester_3,
            semester_4
        ])

        # Module verschiedenen Semestern zuweisen
        semester_1.modules.append(module_python1)
        semester_1.modules.append(module_game_dev)
        semester_2.modules.append(module_sql)
        semester_2.modules.append(module_game_art)
        semester_3.modules.append(module_python2)
        semester_3.modules.append(module_english)
        semester_4.modules.append(module_german)
        semester_4.modules.append(module_unity)

        # Prüfungsergebnisse den Modulen zuweisen
        module_python1.exam_results.append(result1)
        module_python1.exam_results.append(result2)
        module_python2.exam_results.append(result3)
        module_sql.exam_results.append(result4)
        module_english.exam_results.append(result5)
        module_german.exam_results.append(result6)
        module_german.exam_results.append(result7)
        module_game_art.exam_results.append(result8)
        module_game_dev.exam_results.append(result9)
        module_game_dev.exam_results.append(result10)
        module_unity.exam_results.append(result11)

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
            degree_program = DegreeProgram()

    # Application starten.
    application = Application(
        degree_program,
        save_on_close=save_on_close
    )

    application.start()


if __name__ == "__main__":
    main()

