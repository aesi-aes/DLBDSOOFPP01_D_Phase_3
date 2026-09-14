from dataclasses import dataclass, field

from models.exam_result import ExamResult

#Ein Module hällt eine Liste an Prüfungsergebnissen und kann damit abgeschlossen werden.
@dataclass
class Module:
    module_number: str
    name: str
    exam_results: list[ExamResult] = field(default_factory=list)

    @property
    def is_completed(self) -> bool:
        return len(self.exam_results) > 0