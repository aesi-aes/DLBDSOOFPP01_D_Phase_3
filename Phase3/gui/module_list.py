import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from models.semester import Semester


class ModuleList(tk.LabelFrame):
    def __init__(
        self,
        parent,
        controller,
        on_module_selected
    ):
        super().__init__(
            parent,
            text="MODULE",
            padx=10,
            pady=10
        )

        self.controller = controller
        self.on_module_selected_callback = on_module_selected

        self.module_tree = None
        self.tree_items = {}
        self.semester_items = {}

        self.selected_module = None
        self.selected_semester = None

        self.new_semester_button = None
        self.delete_semester_button = None
        self.set_current_semester_button = None

        self.create_widgets()

    def create_widgets(self):
        module_content_frame = tk.Frame(self)
        module_content_frame.pack(
            fill="both",
            expand=True
        )

        self.module_tree = ttk.Treeview(
            module_content_frame,
            columns=("name", "status"),
            show="tree headings"
        )

        self.module_tree.heading("#0", text="Modul")
        self.module_tree.heading("name", text="Name")
        self.module_tree.heading("status", text="Status")

        self.module_tree.bind(
            "<<TreeviewSelect>>",
            self.on_tree_selection_changed
        )

        self.module_tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Semester-Buttons
        semester_button_frame = tk.Frame(
            module_content_frame
        )
        semester_button_frame.pack(
            side="right",
            fill="y",
            padx=(10, 0)
        )

        self.set_current_semester_button = tk.Button(
            semester_button_frame,
            text="Aktuelles\nSemester",
            command=self.on_set_current_semester
        )
        self.set_current_semester_button.pack(
            fill="x"
        )

        self.new_semester_button = tk.Button(
            semester_button_frame,
            text="Neues\nSemester",
            command=self.on_new_semester
        )
        self.new_semester_button.pack(
            fill="x",
            pady=(10, 0)
        )

        self.delete_semester_button = tk.Button(
            semester_button_frame,
            text="Semester\nlöschen",
            command=self.on_delete_semester
        )
        self.delete_semester_button.pack(
            fill="x",
            pady=(10, 0)
        )

    def update(self):
        self.update_tree()
        self.update_controls()

    def update_tree(self):
        # "Geöffnete" Einträge merken.
        open_semesters = set()

        # Semester-Items erstellen
        for item in self.module_tree.get_children():
            if self.module_tree.item(item, "open"):
                open_semesters.add(
                    self.module_tree.item(item, "text")
                )

        # Alte Listeneinträge entfernen
        for item in self.module_tree.get_children():
            self.module_tree.delete(item)

        # Items aufräumen
        self.tree_items.clear()
        self.semester_items.clear()

        semesters = self.controller.study_service.get_semesters()

        for index, semester in enumerate(semesters, start=1):
            semester_item = self.module_tree.insert(
                "",
                "end",
                text=semester.name,
                open=semester.name in open_semesters,
                tags=(
                    ("current_semester",)
                    if index == self.controller.study_service.get_current_semester()
                    else ()
                )
            )

            # Semester-UI-Item merken
            self.semester_items[semester_item] = semester

            # Semester-UI-Item 'bold' markieren, falls aktuelles Semsester.
            self.module_tree.tag_configure(
                "current_semester",
                font=("TkDefaultFont", 10, "bold")
            )

            for module in semester.modules:
                # Modul-Status feststellen
                status = (
                    "Abgeschlossen"
                    if module.is_completed
                    else "Offen"
                )

                # Modul-UI-Entry erstellen
                module_item = self.module_tree.insert(
                    semester_item,
                    "end",
                    text=module.module_number,
                    values=(
                        module.name,
                        status
                    )
                )

                # Element merken
                self.tree_items[module_item] = module

                # Letztes ausgewähltes Modul wieder auswählen
                if module == self.selected_module:
                    self.module_tree.selection_set(module_item)
                    self.module_tree.focus(module_item)

    def on_tree_selection_changed(self, event):
        # Selektion
        selected_items = self.module_tree.selection()

        # Reset falls nichts selektiert
        if not selected_items:
            self.selected_module = None
            self.selected_semester = None

            self.update_controls()

            self.on_module_selected_callback(None)
            return

        selected_item = selected_items[0]

        # Wurde ein Semester ausgewählt?
        semester = self.semester_items.get(selected_item)

        # Semester-Buttons falls Semester selektiert.
        if semester is not None:
            self.selected_semester = semester
            self.selected_module = None

            self.update_controls()

            self.on_module_selected_callback(None)
            return

        # Wurde ein Modul ausgewählt?
        module = self.tree_items.get(selected_item)

        # Reset falls kein Modul ausgewählt
        if module is None:
            self.selected_module = None
            self.selected_semester = None

            self.update_controls()

            self.on_module_selected_callback(None)
            return

        self.selected_module = module
        self.selected_semester = None

        self.update_controls()

        self.on_module_selected_callback(module)

    def update_controls(self):
        has_semester = self.selected_semester is not None

        self.set_current_semester_button.config(
            state="normal" if has_semester else "disabled"
        )

        self.delete_semester_button.config(
            state="normal" if has_semester else "disabled"
        )

    def on_set_current_semester(self):
        if self.selected_semester is None:
            return

        self.controller.on_current_semester_changed(
            self.selected_semester
        )

        self.update()

    def on_new_semester(self):
        name = simpledialog.askstring(
            "Neues Semester",
            "Name des Semesters:"
        )

        if name is None:
            return

        name = name.strip()

        if not name:
            messagebox.showerror(
                "Ungültige Eingabe",
                "Der Semestername darf nicht leer sein."
            )
            return

        semester = Semester(name=name)

        self.controller.on_semester_added(semester)

        self.update()

    def on_delete_semester(self):
        if self.selected_semester is None:
            return

        semester = self.selected_semester

        confirmed = messagebox.askyesno(
            "Semester löschen",
            f"Möchtest du '{semester.name}' wirklich löschen?\n\n"
            "Alle Module und Prüfungsergebnisse dieses Semesters "
            "werden ebenfalls gelöscht."
        )

        if not confirmed:
            return

        try:
            self.controller.on_semester_deleted(semester)
        except ValueError as error:
            messagebox.showerror(
                "Semester kann nicht gelöscht werden",
                str(error)
            )
            return

        self.selected_semester = None
        self.selected_module = None

        self.update()

        self.on_module_selected_callback(None)