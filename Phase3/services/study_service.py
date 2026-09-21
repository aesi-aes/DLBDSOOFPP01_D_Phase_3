from models.degree_program import DegreeProgram
from models.module import Module
from models.semester import Semester


# StudyService ist verantwortlich für Zugriffe auf Modules und weitere Infos (Studienfortschritt etc.)
class StudyService:

    def __init__(self, degree_program: DegreeProgram):
        self.degree_program = degree_program

    def get_total_modules(self) -> int:
        total_modules = 0

        for semester in self.degree_program.semesters:
            total_modules += len(semester.modules)

        return total_modules

    def get_completed_modules(self) -> int:
        completed_modules = 0

        for semester in self.degree_program.semesters:
            for module in semester.modules:
                if module.is_completed:
                    completed_modules += 1

        return completed_modules

    # Studienfortschritt in [0..100] %
    def get_study_progress(self) -> float:
        total_modules = self.get_total_modules()

        if total_modules == 0:
            return 0.0

        completed_modules = self.get_completed_modules()

        return completed_modules / total_modules * 100

    def get_current_semester(self) -> int:
        return self.degree_program.current_semester

    def set_current_semester(self, semester: Semester):
        semester_index = self.degree_program.semesters.index(semester)

        self.degree_program.current_semester = semester_index + 1

    def get_modules(self) -> list[Module]:
        modules = []

        for semester in self.degree_program.semesters:
            modules.extend(semester.modules)

        return modules

    def get_semesters(self) -> list[Semester]:
        return self.degree_program.semesters

    def add_semester(self, semester: Semester):
        self.degree_program.semesters.append(semester)

    def delete_semester(self, semester: Semester):
        if len(self.degree_program.semesters) <= 1:
            raise ValueError(
                "DegreeProgram: Es muss mindestens ein Semester geben!"
            )

        semester_index = self.degree_program.semesters.index(semester)
        current_index = self.degree_program.current_semester - 1

        self.degree_program.semesters.remove(semester)

        # Wenn ein Semester 'vor' dem aktuellen gelöscht wird,
        # current_semester um -1 shiften.
        if semester_index < current_index:
            self.degree_program.current_semester -= 1

        # Wenn das aktuelle Semester gelöscht wird, selbe Index
        # oder den letzten Index.
        elif semester_index == current_index:
            self.degree_program.current_semester = min(
                self.degree_program.current_semester,
                len(self.degree_program.semesters)
            )

    def add_module(self, semester, module):
        semester.add_module(module)

    def delete_module(self, semester, module):
        semester.remove_module(module)