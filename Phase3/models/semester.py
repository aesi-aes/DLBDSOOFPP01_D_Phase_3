from dataclasses import dataclass, field

from models.module import Module

# Das Semester besteht aus mehreren Modulen die abgeschlossen werden können.
@dataclass
class Semester:
    name: str
    modules: list[Module] = field(default_factory=list)