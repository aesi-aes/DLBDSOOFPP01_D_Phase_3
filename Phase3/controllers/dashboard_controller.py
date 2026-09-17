from models.exam_result import ExamResult
from models.exam_type import ExamType
from models.module import Module

from services.study_service import StudyService
from services.grade_service import GradeService


class DashboardController:

    def __init__(
        self,
        study_service: StudyService,
        grade_service: GradeService
    ):
        self.study_service = study_service
        self.grade_service = grade_service

    def on_exam_result_added(
            self,
            module: Module,
            exam_result: ExamResult
    ):
        self.grade_service.add_exam_result(
            module,
            exam_result
        )

    def on_target_average_changed(
            self,
            target_average: float
    ):
        self.grade_service.set_target_average(
            target_average
        )

    def update_exam_result(
        self,
        exam_result: ExamResult,
        exam_type: ExamType,
        grade: float
    ):
        self.grade_service.update_exam_result(
            exam_result,
            exam_type,
            grade
        )