import tkinter as tk

from controllers.dashboard_controller import DashboardController
from tkinter import messagebox

from gui.exam_result_editor import ExamResultEditor
from gui.exam_results import ExamResults
from gui.module_list import ModuleList
from models.exam_result import ExamResult
from models.exam_type import ExamType


class Dashboard:
    def __init__(self, controller: DashboardController):
        self.module_list = None
        self.exam_results = None
        self.exam_result_editor = None

        self.target_status_label = None
        self.target_average_label = None
        self.average_label = None
        self.study_progress_label = None
        self.target_entry = None
        self.controller = controller

        self.root = tk.Tk()
        self.root.title("COURSE DASHBOARD")
        self.root.geometry("900x950")

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

        self.study_progress_label = tk.Label(
            study_frame,
            font=("Arial", 32, "bold")
        )
        self.study_progress_label.pack()

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

        self.average_label = tk.Label(
            grade_frame,
            font=("Arial", 32, "bold")
        )
        self.average_label.pack()

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

        # Liste der Module
        self.module_list = ModuleList(main_frame, self.controller, self.on_module_selected, self.on_module_added, self.on_module_deleted)
        self.module_list.pack(
            fill="both",
            expand=True,
            pady=(20, 0)
        )

        # Prüfungsergebnisse.
        self.exam_results = ExamResults(
            main_frame,
            self.controller,
            on_result_selected=self.on_exam_result_selected,
            on_new_result=self.on_new_exam_result,
            get_selected_module=lambda: self.module_list.selected_module
        )
        self.exam_results.pack(
            fill="x",
            pady=(10, 0)
        )

        # Ergebnis-Editor.
        self.exam_result_editor = ExamResultEditor(
            main_frame,
            on_save=self.on_save_exam_result
        )
        self.exam_result_editor.pack(
            fill="x",
            pady=(10, 0)
        )

        self.update_dashboard()

    def update_dashboard(self):
        self.update_study_progress()
        self.update_average()
        self.update_target_display()
        self.module_list.update()
        self.exam_results.update()

    def update_study_progress(self):
        study_progress = self.controller.study_service.get_study_progress()

        self.study_progress_label.config(text=f"{study_progress:.1f}%")

    def update_average(self):
        average = self.controller.grade_service.get_current_average()

        self.average_label.config(text=f"{average:.2f}")

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

    def on_module_selected(self, module):
        self.exam_results.update(module)
        self.exam_result_editor.update()

    def on_module_added(self, semester, module):
        self.controller.on_module_added(semester, module)
        self.update_dashboard()

    def on_module_deleted(self, semester, module):
        self.controller.on_module_deleted(semester, module)
        self.update_dashboard()

    def on_set_target_average(self):
        # float-Zahl soll abgefragt werden, falls nicht: Fehlermeldung
        try:
            target_average = float(self.target_entry.get())
        except ValueError:
            messagebox.showerror(
                "Ungültige Eingabe",
                "Bitte eine gültige Zahl angeben.",
                icon="error"
            )
            return

        # falls Zahl nicht zwischen 1-6
        try:
            self.controller.on_target_average_changed(target_average)
        except ValueError as error:
            messagebox.showerror(
                "Ungültige Eingabe",
                str(error),
                icon="error"
            )
            return

        self.update_target_display()

    def on_exam_result_selected(self, result):
        self.exam_result_editor.update(exam_result=result)

    def on_new_exam_result(self):
        if self.module_list.selected_module is None:
            return

        self.exam_result_editor.update(is_creating=True)
        self.exam_result_editor.focus()

    def on_save_exam_result(self, exam_type_value, grade_value):
        module = self.module_list.selected_module

        # Error Handling:
        if module is None:
            messagebox.showinfo(
                "Kein Modul ausgewählt",
                "Bitte wähle zuerst ein Modul aus.",
                icon="info"
            )
            return

        if not exam_type_value:
            messagebox.showerror(
                "Ungültige Eingabe",
                "Bitte wähle eine Prüfungsart aus.",
                icon="error"
            )
            return

        if grade_value.strip() == "":
            grade = None
        else:
            try:
                grade = float(grade_value)
            except ValueError:
                messagebox.showerror(
                    "Ungültige Eingabe",
                    "Bitte gib eine gültige Note (von 1-6) ein.",
                    icon="error"
                )
                return

        # Werte auslesen
        exam_type = ExamType(exam_type_value)
        existing_result = self.exam_result_editor.exam_result

        try:
            # Result bearbeiten oder neu hinzufügen
            if existing_result is None:
                exam_result = ExamResult(exam_type=exam_type, grade=grade)
                self.controller.on_exam_result_added(module, exam_result)
            else:
                self.controller.update_exam_result(existing_result, exam_type, grade)
        except ValueError as error:
            # Error Handling
            messagebox.showerror(
                "Ungültige Eingabe",
                str(error),
                icon="error"
            )
            return

        # UI aktualisieren
        self.exam_result_editor.update()
        self.update_dashboard()

    def show(self):
        self.root.mainloop()
