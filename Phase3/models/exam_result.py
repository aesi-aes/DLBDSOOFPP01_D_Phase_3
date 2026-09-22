from dataclasses import dataclass

from models.exam_type import ExamType

# Ein Prüfungsergebnis enthält die Note und kann abgeschlossen werden.
@dataclass
class ExamResult:
    exam_type: ExamType
    grade: float | None = None

    @property
    def is_passed(self) -> bool:
        return self.grade is not None and self.grade <= 4.0