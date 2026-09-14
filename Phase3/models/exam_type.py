from enum import Enum

# Bildet verschiedene Typen von Prüfungen ab.
class ExamType(Enum):
    ONLINE_TEST = "OnlineTest"
    PROJECT = "Project"
    MANUSCRIPT = "Manuscript"