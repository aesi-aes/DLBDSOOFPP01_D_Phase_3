from controllers.dashboard_controller import DashboardController
from data.config import DATA_FILE
from data.json_data_store import JsonDataStore
from gui.dashboard import Dashboard
from services.grade_service import GradeService
from services.study_service import StudyService


class Application:
    def __init__(self, degree_program, save_on_close=True):
        self.degree_program = degree_program
        self.save_on_close = save_on_close

        self.data_store = JsonDataStore(DATA_FILE)

        self.study_service = StudyService(
            self.degree_program
        )

        self.grade_service = GradeService(
            self.degree_program
        )

        self.dashboard_controller = DashboardController(
            self.study_service,
            self.grade_service
        )

        self.dashboard = Dashboard(
            self.dashboard_controller
        )

        # Event -> Schließen der App
        self.dashboard.root.protocol(
            "WM_DELETE_WINDOW",
            self.on_close
        )

    def start(self):
        self.dashboard.show()

    def on_close(self):
        # JSON-Daten speichern.
        if self.save_on_close:
            self.data_store.save(
                self.degree_program
            )

        self.dashboard.root.destroy()
