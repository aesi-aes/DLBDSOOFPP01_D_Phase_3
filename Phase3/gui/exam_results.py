import tkinter as tk
from tkinter import messagebox, ttk


class ExamResults(tk.LabelFrame):
    def __init__(
        self,
        parent,
        controller,
        on_result_selected,
        on_new_result,
        on_delete_result,
        get_selected_module
    ):
        super().__init__(
            parent,
            text="PRÜFUNGSERGEBNISSE",
            padx=10,
            pady=10
        )

        self.controller = controller
        self.on_result_selected_callback = on_result_selected
        self.on_new_result_callback = on_new_result
        self.on_delete_result_callback = on_delete_result
        self.get_selected_module = get_selected_module

        self.exam_results_tree = None
        self.exam_result_items = {}

        self.new_result_button = None
        self.delete_result_button = None

        self.selected_result = None

        self.create_widgets()

    def create_widgets(self):
        exam_result_content_frame = tk.Frame(self)
        exam_result_content_frame.pack(
            fill="x",
            pady=(0, 10)
        )

        # Liste der Prüfungsergebnisse + Scrollbar
        exam_result_tree_frame = tk.Frame(
            exam_result_content_frame
        )
        exam_result_tree_frame.pack(
            side="left",
            fill="x",
            expand=True
        )

        self.exam_results_tree = ttk.Treeview(
            exam_result_tree_frame,
            columns=("exam_type", "grade", "status"),
            show="headings",
            height=4
        )
        self.exam_results_tree.heading(
            "exam_type",
            text="Prüfungsart"
        )
        self.exam_results_tree.heading(
            "grade",
            text="Note"
        )
        self.exam_results_tree.heading(
            "status",
            text="Status"
        )
        self.exam_results_tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Vertikale Scrollbar
        scrollbar = ttk.Scrollbar(
            exam_result_tree_frame,
            orient="vertical",
            command=self.exam_results_tree.yview
        )
        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.exam_results_tree.configure(
            yscrollcommand=scrollbar.set
        )
        self.exam_results_tree.bind(
            "<<TreeviewSelect>>",
            self.on_result_tree_selected
        )

        # Buttons
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
            command=self.on_new_result
        )
        self.new_result_button.pack(fill="x")

        self.delete_result_button = tk.Button(
            exam_result_button_frame,
            text="Ergebnis\nlöschen",
            command=self.on_delete_result
        )
        self.delete_result_button.pack(
            fill="x",
            pady=(10, 0)
        )

        self.update_controls()

    # UI updaten
    def update(self, module=None):
        if module is None:
            module = self.get_selected_module()

        self.clear()

        # Reset wenn kein Modul selektiert.
        if module is None:
            self.selected_result = None
            self.update_controls()
            return

        # Result Liste aufbauen.
        for result in module.exam_results:
            grade_string = "-" if result.grade is None else f"{result.grade:.1f}"
            status_string = (
                "Bestanden"
                if result.is_passed
                else "Noch nicht geprüft"
                if result.grade is None
                else "Nicht bestanden"
            )
            item = self.exam_results_tree.insert(
                "",
                "end",
                values=(result.exam_type.value, grade_string, status_string)
            )

            self.exam_result_items[item] = result

        self.selected_result = None
        self.update_controls()

    # UI-Einträge leeren / löschen
    def clear(self):
        # Liste der Prüfungsergebnisse löschen
        for item in self.exam_results_tree.get_children():
            self.exam_results_tree.delete(item)

        self.exam_result_items.clear()

    # UI-Update
    def update_controls(self):
        has_module = self.get_selected_module() is not None
        has_result = self.selected_result is not None

        # Buttons enablen/disablen
        self.new_result_button.config(
            state="normal" if has_module else "disabled"
        )

        self.delete_result_button.config(
            state="normal" if has_result else "disabled"
        )

    # UI-Selektion des Ergebnis Trees
    def on_result_tree_selected(self, event):
        # UI-Selektion.
        selected_items = self.exam_results_tree.selection()

        # Reset und Callback wenn nichts selektiert.
        if not selected_items:
            self.selected_result = None
            self.update_controls()

            self.on_result_selected_callback(None)
            return

        selected_item = selected_items[0]
        result = self.exam_result_items.get(selected_item)

        # Kein Result -> Controls Reset
        if result is None:
            self.selected_result = None
            self.update_controls()
            return

        self.selected_result = result
        self.update_controls()

        self.on_result_selected_callback(result)

    # Neues Prüfungsergebnis
    def on_new_result(self):
        if self.get_selected_module() is None:
            return

        self.selected_result = None
        self.update_controls()

        self.on_new_result_callback()

    # Prüfungsergebnis löschen
    def on_delete_result(self):
        module = self.get_selected_module()

        # Fehlermeldung
        if module is None:
            messagebox.showinfo(
                "Kein Modul ausgewählt",
                "Bitte wähle zuerst ein Modul aus.",
                icon="question"
            )
            return

        result = self.selected_result

        # Fehlermeldung
        if result is None:
            messagebox.showinfo(
                "Kein Ergebnis ausgewählt",
                "Bitte wähle zuerst ein Prüfungsergebnis aus.",
                icon="question"
            )
            return

        # Löschen bestätigen
        confirmed = messagebox.askyesno(
            "Prüfungsergebnis löschen",
            "Möchtest du dieses Prüfungsergebnis wirklich löschen?",
            icon="warning"
        )

        if not confirmed:
            return

        self.on_delete_result_callback(result)