import tkinter as tk

from controllers.dashboard_controller import DashboardController
from tkinter import messagebox, ttk, simpledialog

from gui.module_list import ModuleList
from models.exam_result import ExamResult
from models.exam_type import ExamType
from models.semester import Semester


class Dashboard:
    def __init__(self, controller: DashboardController):
        self.module_list = None

        self.exam_results_tree = None
        self.exam_result_items = {}

        self.new_result_button = None
        self.delete_result_button = None
        self.save_result_button = None
        self.editing_exam_result = None
        self.is_creating_exam_result = False

        self.exam_type_combobox = None
        self.target_status_label = None
        self.grade_entry = None

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
        self.module_list = ModuleList(main_frame, self.controller, self.on_module_selected)
        self.module_list.pack(
            fill="both",
            expand=True,
            pady=(20, 0)
        )

        # Prüfungsergebnisse.
        results_frame = tk.LabelFrame(
            main_frame,
            text="PRÜFUNGSERGEBNISSE",
            padx=10,
            pady=10
        )
        results_frame.pack(
            fill="x",
            pady=(10, 0)
        )

        exam_result_content_frame = tk.Frame(
            results_frame
        )
        exam_result_content_frame.pack(
            fill="x",
            pady=(0, 10)
        )

        self.exam_results_tree = ttk.Treeview(
            exam_result_content_frame,
            columns=("exam_type", "grade", "status"),
            show="headings",
            height=4
        )
        self.exam_results_tree.heading("exam_type", text="Prüfungsart")
        self.exam_results_tree.heading("grade", text="Note")
        self.exam_results_tree.heading("status", text="Status")
        self.exam_results_tree.pack(
            side="left",
            fill="x",
            expand=True
        )

        self.exam_results_tree.bind(
            "<<TreeviewSelect>>",
            self.on_exam_result_selected
        )

        # Prüfungsergebnis bearbeiten
        exam_result_button_frame = tk.Frame(
            exam_result_content_frame
        )
        exam_result_button_frame.pack(
            side="right",
            fill="y",
            padx=(10, 0)
        )

        self.new_result_button = tk.Button(
            exam_result_button_frame,
            text="Neues\nErgebnis",
            command=self.on_new_exam_result
        )
        self.new_result_button.pack(fill="x")

        self.delete_result_button = tk.Button(
            exam_result_button_frame,
            text="Ergebnis\nlöschen",
            command=self.on_delete_exam_result
        )
        self.delete_result_button.pack(fill="x", pady=(10, 0))

        exam_result_editor_frame = tk.LabelFrame(
            results_frame,
            text="PRÜFUNGSERGEBNIS BEARBEITEN",
            padx=10,
            pady=10
        )
        exam_result_editor_frame.pack(fill="x", pady=(10, 0))

        tk.Label(
            exam_result_editor_frame,
            text="Prüfungsart:"
        ).grid(row=0, column=0, sticky="w", padx=(0, 10))

        self.exam_type_combobox = ttk.Combobox(
            exam_result_editor_frame,
            values=[
                exam_type.value
                for exam_type in ExamType
            ],
            state="readonly"
        )
        self.exam_type_combobox.grid(
            row=0,
            column=1,
            sticky="ew"
        )

        tk.Label(
            exam_result_editor_frame,
            text="Note:"
        ).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(10, 0))

        self.grade_entry = tk.Entry(exam_result_editor_frame)
        self.grade_entry.grid(
            row=1,
            column=1,
            sticky="ew",
            pady=(10, 0)
        )

        exam_result_editor_frame.columnconfigure(1, weight=1)

        self.save_result_button = tk.Button(
            exam_result_editor_frame,
            text="Speichern",
            command=self.on_save_exam_result
        )
        self.save_result_button.grid(
            row=2,
            column=1,
            sticky="e",
            pady=(10, 0)
        )

        self.update_dashboard()

    def get_selected_module(self):
        return self.module_list.selected_module

    def update_dashboard(self):
        self.update_study_progress()
        self.update_average()
        self.update_target_display()
        self.module_list.update()
        self.update_exam_result_controls()

    def update_study_progress(self):
        study_progress = self.controller.study_service.get_study_progress()

        self.study_progress_label.config(
            text=f"{study_progress:.1f}%",
        )

    def update_average(self):
        average = self.controller.grade_service.get_current_average()

        self.average_label.config(
            text=f"{average:.2f}"
        )

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

    def update_module_tree(self):
        # "Geöffnete" Einträge merken.
        open_semesters = set()
        for item in self.module_tree.get_children():
            if self.module_tree.item(item, "open"):
                open_semesters.add(
                    self.module_tree.item(item, "text")
                )

        # Alte Listeneinträge entfernen
        for item in self.module_tree.get_children():
            self.module_tree.delete(item)

        # Tree leeren
        self.tree_items.clear()

        semesters = self.controller.study_service.get_semesters()

        for index, semester in enumerate(semesters, start=1):
            # Neuer Semester-Eintrag (geöffnet falls in open_semesters)
            semester_item = self.module_tree.insert(
                "",
                "end",
                text=semester.name,
                open=semester.name in open_semesters,
                tags=("current_semester",)
                if index == self.controller.study_service.get_current_semester()
                else ()
            )

            self.semester_items[semester_item] = semester

            self.module_tree.tag_configure(
                "current_semester",
                font=("TkDefaultFont", 10, "bold")
            )

            # Module anzeigen
            for module in semester.modules:
                if module.is_completed:
                    status = "Abgeschlossen"
                else:
                    status = "Offen"

                module_item = self.module_tree.insert(
                    semester_item,
                    "end",
                    text=module.module_number,
                    values=(
                        module.name,
                        status
                    )
                )

                self.tree_items[module_item] = module

                # Letztes ausgewähltes Modul wieder auswählen
                if module == self.module_list.selected_module:
                    self.module_tree.selection_set(module_item)
                    self.module_tree.focus(module_item)

    def update_semester_controls(self):
        has_semester = self.selected_semester is not None

        self.set_current_semester_button.config(
            state="normal" if has_semester else "disabled"
        )

        self.delete_semester_button.config(
            state="normal" if has_semester else "disabled"
        )

    def update_exam_result_controls(self):
        # Was ist selektiert?
        has_module = self.module_list.selected_module is not None
        has_result = self.editing_exam_result is not None
        editor_active = has_result or self.is_creating_exam_result

        # Buttons de/aktivieren.
        self.new_result_button.config(
            state="normal" if has_module else "disabled"
        )
        self.delete_result_button.config(
            state="normal" if has_result else "disabled"
        )

        # Ergebnis-Editor nur editierbar wenn ein ExamResult bearbeitet wird.
        self.exam_type_combobox.config(
            state="readonly" if editor_active else "disabled"
        )
        self.grade_entry.config(
            state="normal" if editor_active else "disabled"
        )
        self.save_result_button.config(
            state="normal" if editor_active else "disabled"
        )

    def on_module_selected(self, module):
        if module is None:
            self.clear_exam_results()
            self.editing_exam_result = None
            self.is_creating_exam_result = False
            self.clear_exam_result_editor()
            self.update_exam_result_controls()
            return

        self.show_exam_results(module)

    def show_exam_results(self, module):
        self.module_list.selected_module = module

        # Bearbeiten-Status zurücksetzen
        self.editing_exam_result = None
        self.is_creating_exam_result = False

        # alle Einträge löschen
        self.clear_exam_results()

        # neue Einträge erstellen
        for result in module.exam_results:
            item = self.exam_results_tree.insert(
                "",
                "end",
                values=(
                    result.exam_type.value,
                    f"{result.grade:.1f}",
                    "Bestanden" if result.is_passed else "Nicht bestanden"
                )
            )

            self.exam_result_items[item] = result

        # UI-Elemente zurücksetzen
        self.clear_exam_result_editor()
        self.update_exam_result_controls()

    def clear_exam_result_editor(self):
        # Ergebnis-Editor zurücksetzen
        self.exam_type_combobox.set("")
        self.grade_entry.delete(0, tk.END)

    def clear_exam_results(self):
        # alle Einträge löschen
        for item in self.exam_results_tree.get_children():
            self.exam_results_tree.delete(item)

        # alle Items löschen
        self.exam_result_items.clear()

    def on_set_target_average(self):
        # float-Zahl soll abgefragt werden, falls nicht: Fehlermeldung
        try:
            target_average = float(self.target_entry.get())
        except ValueError:
            messagebox.showerror(
                "Ungültige Eingabe",
                "Bitte eine gültige Zahl angeben."
            )
            return

        # falls Zahl nicht zwischen 1-6
        try:
            self.controller.on_target_average_changed(target_average)
        except ValueError as error:
            messagebox.showerror(
                "Ungültige Eingabe",
                str(error)
            )
            return

        self.update_target_display()

    def on_exam_result_selected(self, event):
        if self.is_creating_exam_result:
            return

        selected_items = self.exam_results_tree.selection()

        if not selected_items:
            self.editing_exam_result = None
            self.is_creating_exam_result = False
            self.clear_exam_result_editor()
            self.update_exam_result_controls()
            return

        selected_item = selected_items[0]

        result = self.exam_result_items.get(selected_item)

        if result is None:
            return

        self.editing_exam_result = result
        self.is_creating_exam_result = False

        self.exam_type_combobox.set(
            self.editing_exam_result.exam_type.value
        )

        self.grade_entry.delete(0, tk.END)
        self.grade_entry.insert(
            0,
            str(self.editing_exam_result.grade)
        )

        self.update_exam_result_controls()

    def on_new_exam_result(self):
        if self.module_list.selected_module is None:
            return

        self.editing_exam_result = None
        self.is_creating_exam_result = True

        self.clear_exam_result_editor()
        self.update_exam_result_controls()

        self.exam_type_combobox.focus_set()

    def on_save_exam_result(self):
        if self.module_list.selected_module is None:
            messagebox.showinfo(
                "Kein Modul ausgewählt",
                "Bitte wähle zuerst ein Modul aus."
            )
            return

        exam_type_value = self.exam_type_combobox.get()

        if not exam_type_value:
            messagebox.showerror(
                "Ungültige Eingabe",
                "Bitte wähle eine Prüfungsart aus."
            )
            return

        try:
            grade = float(self.grade_entry.get())
        except ValueError:
            messagebox.showerror(
                "Ungültige Eingabe",
                "Bitte gib eine gültige Note (von 1-6) ein."
            )
            return

        exam_type = ExamType(exam_type_value)

        try:
            if self.editing_exam_result is None:
                exam_result = ExamResult(
                    exam_type=exam_type,
                    grade=grade
                )

                self.controller.on_exam_result_added(
                    self.module_list.selected_module,
                    exam_result
                )
            else:
                self.controller.update_exam_result(
                    self.editing_exam_result,
                    exam_type,
                    grade
                )

        except ValueError as error:
            messagebox.showerror(
                "Ungültige Eingabe",
                str(error)
            )
            return

        self.show_exam_results(self.module_list.selected_module)
        self.editing_exam_result = None
        self.is_creating_exam_result = False
        self.clear_exam_result_editor()
        self.update_dashboard()

    def on_delete_exam_result(self):
        if self.module_list.selected_module is None:
            messagebox.showinfo(
                "Kein Modul ausgewählt",
                "Bitte wähle zuerst ein Modul aus."
            )
            return

        selected_items = self.exam_results_tree.selection()

        if not selected_items:
            messagebox.showinfo(
                "Kein Ergebnis ausgewählt",
                "Bitte wähle zuerst ein Prüfungsergebnis aus."
            )
            return

        selected_item = selected_items[0]

        result = self.exam_result_items.get(selected_item)

        if result is None:
            return

        confirmed = messagebox.askyesno(
            "Prüfungsergebnis löschen",
            "Möchtest du dieses Prüfungsergebnis wirklich löschen?"
        )

        if not confirmed:
            return

        self.controller.on_exam_result_deleted(
            self.module_list.selected_module,
            result
        )

        self.show_exam_results(self.module_list.selected_module)

        self.editing_exam_result = None
        self.exam_type_combobox.set("")
        self.grade_entry.delete(0, tk.END)
        self.update_dashboard()

    def show(self):
        self.root.mainloop()
