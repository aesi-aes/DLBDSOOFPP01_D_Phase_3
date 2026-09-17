import tkinter as tk

from controllers.dashboard_controller import DashboardController
from tkinter import messagebox, ttk

class Dashboard:
    def __init__(self, controller: DashboardController):
        self.module_tree = None
        self.tree_items = {}

        self.selected_module = None
        self.exam_results_tree = None
        self.exam_result_items = {}

        self.target_average_label = None
        self.study_progress_label = None
        self.target_entry = None
        self.controller = controller

        self.root = tk.Tk()
        self.root.title("COURSE DASHBOARD")
        self.root.geometry("900x900")

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
        modules_frame = tk.LabelFrame(
            main_frame,
            text="MODULE",
            padx=10,
            pady=10
        )
        modules_frame.pack(
            fill="both",
            expand=True,
            pady=(20, 0)
        )

        self.module_tree = ttk.Treeview(
            modules_frame,
            columns=("name", "status"),
            show="tree headings"
        )

        self.module_tree.heading("#0", text="Modul")
        self.module_tree.heading("name", text="Name")
        self.module_tree.heading("status", text="Status")

        self.module_tree.bind(
            "<<TreeviewSelect>>",
            self.on_module_selected
        )

        self.module_tree.pack(
            fill="both",
            expand=True
        )

        # Prüfungsergebnisse.
        results_frame = tk.LabelFrame(
            modules_frame,
            text="PRÜFUNGSERGEBNISSE",
            padx=10,
            pady=10
        )
        results_frame.pack(
            fill="x",
            pady=(10, 0)
        )

        self.exam_results_tree = ttk.Treeview(
            results_frame,
            columns=("exam_type", "grade", "status"),
            show="headings",
            height=4
        )
        self.exam_results_tree.heading("exam_type", text="Prüfungsart")
        self.exam_results_tree.heading("grade", text="Note")
        self.exam_results_tree.heading("status", text="Status")
        self.exam_results_tree.pack(
            fill="x",
            pady=(0, 10)
        )
        self.exam_results_tree.bind(
            "<<TreeviewSelect>>",
            self.on_exam_result_selected
        )

        self.update_dashboard()

    def update_dashboard(self):
        self.update_study_progress()
        self.update_average()
        self.update_target_display()
        self.update_module_tree()

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
        # Alte Listeneinträge entfernen
        for item in self.module_tree.get_children():
            self.module_tree.delete(item)

        # Tree leeren
        self.tree_items.clear()

        semesters = self.controller.study_service.get_semesters()

        for semester in semesters:
            semester_item = self.module_tree.insert(
                "",
                "end",
                text=semester.name
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

    def on_module_selected(self, event):
        selected_items = self.module_tree.selection()

        if not selected_items:
            return

        selected_item = selected_items[0]

        module = self.tree_items.get(selected_item)

        if module is None:
            return

        self.show_exam_results(module)


    def show_exam_results(self, module):
        self.selected_module = module

        for item in self.exam_results_tree.get_children():
            self.exam_results_tree.delete(item)

        self.exam_result_items.clear()

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

        self.update_target_display()

    def on_exam_result_selected(self, event):
        selected_items = self.exam_results_tree.selection()

        if not selected_items:
            return

        selected_item = selected_items[0]

        values = self.exam_results_tree.item(
            selected_item,
            "values"
        )

        print(values)

    def show(self):
        self.root.mainloop()
