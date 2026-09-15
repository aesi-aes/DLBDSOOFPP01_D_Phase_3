from models.degree_program import DegreeProgram
from models.module import Module


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

    def get_modules(self) -> list[Module]:
        modules = []

        for semester in self.degree_program.semesters:
            modules.extend(semester.modules)

        return modules