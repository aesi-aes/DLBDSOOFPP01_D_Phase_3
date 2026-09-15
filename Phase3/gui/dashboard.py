import tkinter as tk

from controllers.dashboard_controller import DashboardController


class Dashboard:
    def __init__(self, controller: DashboardController):
        self.controller = controller

        self.root = tk.Tk()
        self.root.title("COURSE DASHBOARD")
        self.root.geometry("900x600")

        self.create_widgets()

    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title_label = tk.Label(
            main_frame,
            text="COURSE DASHBOARD",
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=(0, 30))

        # Dashboard cards
        cards_frame = tk.Frame(main_frame)
        cards_frame.pack(fill="x")

        # Study progress card
        study_frame = tk.LabelFrame(
            cards_frame,
            text="STUDIENFORTSCHRITT",
            padx=20,
            pady=20
        )
        study_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        study_progress = self.controller.study_service.get_study_progress()

        study_progress_label = tk.Label(
            study_frame,
            text=f"{study_progress:.1f}%",
            font=("Arial", 32, "bold")
        )
        study_progress_label.pack()

        # Average grade card
        grade_frame = tk.LabelFrame(
            cards_frame,
            text="NOTENDURCHSCHNITT",
            padx=20,
            pady=20
        )
        grade_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(10, 0)
        )

        average = self.controller.grade_service.get_current_average()

        average_label = tk.Label(
            grade_frame,
            text=f"{average:.2f}",
            font=("Arial", 32, "bold")
        )
        average_label.pack()

    def show(self):
        self.root.mainloop()