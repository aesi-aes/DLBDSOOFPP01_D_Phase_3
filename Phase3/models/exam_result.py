from dataclasses import dataclass

from models.exam_type import ExamType

# Ein Prüfungsergebnis enthält die Note und kann abgeschlossen werden.
@dataclass
class ExamResult:
    exam_type: ExamType
    grade: float
