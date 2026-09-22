import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from models.module import Module
from models.semester import Semester


class ModuleList(tk.LabelFrame):
    def __init__(
        self,
        parent,
        controller,
        on_module_selected,
        on_module_added,
        on_module_deleted
    ):
        super().__init__(
            parent,
            text="MODULE",
            padx=10,
            pady=10
        )

        self.controller = controller
        self.on_module_selected_callback = on_module_selected
        self.on_module_added_callback = on_module_added
        self.on_module_deleted_callback = on_module_deleted

        self.module_tree = None
        self.tree_items = {}
        self.semester_items = {}

        self.selected_module = None
        self.selected_semester = None

        self.new_semester_button = None
        self.delete_semester_button = None
        self.set_current_semester_button = None

        self.new_module_button = None
        self.delete_module_button = None

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

        separator = ttk.Separator(
            semester_button_frame,
            orient="horizontal"
        )
        separator.pack(
            fill="x",
            pady=10
        )

        self.new_module_button = tk.Button(
            semester_button_frame,
            text="Modul\nhinzufügen",
            command=self.on_new_module
        )
        self.new_module_button.pack(
            fill="x"
        )

        self.delete_module_button = tk.Button(
            semester_button_frame,
            text="Modul\nlöschen",
            command=self.on_delete_module
        )
        self.delete_module_button.pack(
            fill="x",
            pady=(10, 0)
        )

    def update(self):
        self.update_tree()
        self.update_controls()

    def update_tree(self):
        # "Geöffnete" Einträge merken.
        open_semesters = {
            semester.name
            for item, semester in self.semester_items.items()
            if self.module_tree.exists(item)
               and self.module_tree.item(item, "open")
        }

        semesters = self.controller.study_service.get_semesters()

        # Aktuellen Semester-Index merken
        current_semester_index = (
            self.controller.study_service.get_current_semester() - 1
        )

        # Aktuelles Semester immer geöffnet halten
        if semesters and current_semester_index < len(semesters):
            open_semesters.add(semesters[current_semester_index].name)

        # Alte Listeneinträge entfernen
        for item in self.module_tree.get_children():
            self.module_tree.delete(item)

        # Items aufräumen
        self.tree_items.clear()
        self.semester_items.clear()

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

        self.update_controls()

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
        has_module = self.selected_module is not None

        self.set_current_semester_button.config(
            state="normal" if has_semester else "disabled"
        )

        self.delete_semester_button.config(
            state="normal" if has_semester else "disabled"
        )

        self.new_module_button.config(
            state="normal" if has_semester else "disabled"
        )

        self.delete_module_button.config(
            state="normal" if has_module else "disabled"
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
            "werden ebenfalls gelöscht.",
            icon="warning"
        )

        if not confirmed:
            return

        try:
            self.controller.on_semester_deleted(semester)
        except ValueError as error:
            messagebox.showerror(
                "Semester kann nicht gelöscht werden",
                str(error),
                icon="error"
            )
            return

        self.selected_semester = None
        self.selected_module = None

        self.update()

        self.on_module_selected_callback(None)

    def on_new_module(self):
        if self.selected_semester is None:
            return

        dialog = tk.Toplevel(self)
        dialog.title("Modul bearbeiten")
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        tk.Label(
            dialog,
            text="Modulnummer:"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=(10, 5),
            sticky="w"
        )

        module_number_entry = tk.Entry(dialog)
        module_number_entry.grid(
            row=0,
            column=1,
            padx=10,
            pady=(10, 5)
        )

        tk.Label(
            dialog,
            text="Modulname:"
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=5,
            sticky="w"
        )

        module_name_entry = tk.Entry(dialog)
        module_name_entry.grid(
            row=1,
            column=1,
            padx=10,
            pady=5
        )

        def save():
            module_number = module_number_entry.get().strip()
            module_name = module_name_entry.get().strip()

            if not module_number:
                messagebox.showerror(
                    "Ungültige Eingabe",
                    "Die Modulnummer darf nicht leer sein.",
                    parent=dialog,
                    icon="error"
                )
                return

            if not module_name:
                messagebox.showerror(
                    "Ungültige Eingabe",
                    "Der Modulname darf nicht leer sein.",
                    parent=dialog,
                    icon="error"
                )
                return

            module = Module(
                module_number=module_number,
                name=module_name
            )

            try:
                self.on_module_added_callback(
                    self.selected_semester,
                    module
                )
            except ValueError as error:
                messagebox.showerror(
                    "Modul kann nicht hinzugefügt werden",
                    str(error),
                    parent=dialog,
                    icon="error"
                )
                return

            dialog.destroy()

        button_frame = tk.Frame(dialog)
        button_frame.grid(
            row=2,
            column=0,
            columnspan=2,
            pady=10
        )

        tk.Button(
            button_frame,
            text="Speichern",
            command=save
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="Abbrechen",
            command=dialog.destroy
        ).pack(
            side="left",
            padx=5
        )

        module_number_entry.focus_set()

    def on_delete_module(self):
        if self.selected_module is None:
            return

        module = self.selected_module

        # Dialog: Willst du wirklich löschen?
        confirmed = messagebox.askyesno(
            "Modul löschen",
            f"Möchtest du '{module.name}' wirklich löschen?\n\n"
            "Alle Prüfungsergebnisse dieses Moduls werden ebenfalls gelöscht.",
            icon="warning"
        )

        if not confirmed:
            return

        try:
            self.on_module_deleted_callback(self.selected_semester, module)
        except ValueError as error:
            messagebox.showerror(
                "Modul kann nicht gelöscht werden",
                str(error),
                icon="error"
            )
            return