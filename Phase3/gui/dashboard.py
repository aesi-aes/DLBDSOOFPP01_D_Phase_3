import tkinter as tk

from controllers.dashboard_controller import DashboardController
from tkinter import messagebox

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

        # Ziel-Notendurchschnitt

        target_frame = tk.LabelFrame(
            cards_frame,
            text="ZIEL-NOTENDURCHSCHNITT",
            padx=20,
            pady=20
        )
        target_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(10, 0)
        )

        self.target_average_label = tk.Label(
            target_frame,
            font=("Arial", 32, "bold")
        )
        self.target_average_label.pack()

        self.target_entry = tk.Entry(
            target_frame,
            width=10,
            justify="center"
        )
        self.target_entry.pack(pady=(10, 5))

        self.target_entry.insert(
            0,
            str(self.controller.grade_service.get_target_average())
        )

        set_target_button = tk.Button(
            target_frame,
            text="Ziel setzen",
            command=self.on_set_target_average
        )
        set_target_button.pack()

        self.target_status_label = tk.Label(
            target_frame,
            font=("Arial", 12)
        )
        self.target_status_label.pack(pady=(10, 0))

        self.update_target_display()

    def on_set_target_average(self):
        try:
            target_average = float(self.target_entry.get())
        except ValueError:
            messagebox.showerror(
                "Ungültige Eingabe",
                "Bitte eine gültige Zahl angeben."
            )
            return

        try:
            self.controller.on_target_average_changed(target_average)
        except ValueError as error:
            messagebox.showerror(
                "Ungültige Eingabe",
                str(error)
            )
            return

        self.controller.on_target_average_changed(target_average)
        self.update_target_display()

    def show(self):
        self.root.mainloop()

    def update_target_display(self):
        target_average = (
            self.controller.grade_service.get_target_average()
        )

        self.target_average_label.config(
            text=f"{target_average:.2f}"
        )

        if self.controller.grade_service.has_reached_target_average():
            status_text = "Ziel erreicht"
        else:
            status_text = "Ziel noch nicht erreicht"

        self.target_status_label.config(
            text=status_text
        )