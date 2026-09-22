from dataclasses import dataclass, field

from models.semester import Semester

# Das Studienfach hält eine Liste an Semestern, und welches Semester aktuell ist.
@dataclass
class DegreeProgram:
    name: str
    semesters: list[Semester] = field(default_factory=list)
    current_semester: int = 1
    target_average_grade: float = 2.0