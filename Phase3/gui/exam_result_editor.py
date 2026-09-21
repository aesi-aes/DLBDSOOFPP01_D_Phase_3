import tkinter as tk
from tkinter import ttk

from models.exam_type import ExamType

class ExamResultEditor(tk.LabelFrame):

    def __init__(
        self,
        parent,
        on_save
    ):
        self.exam_result = None
        self.is_creating = False

        super().__init__(
            parent,
            text="PRÜFUNGSERGEBNIS BEARBEITEN",
            padx=10,
            pady=10
        )

        self.on_save_callback = on_save

        self.exam_type_combobox = None
        self.grade_entry = None
        self.save_result_button = None

        self.create_widgets()

    def create_widgets(self):
        tk.Label(
            self,
            text="Prüfungsart:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 10)
        )

        self.exam_type_combobox = ttk.Combobox(
            self,
            values=[
                exam_type.value
                for exam_type in ExamType
            ],
            state="disabled"
        )
        self.exam_type_combobox.grid(
            row=0,
            column=1,
            sticky="ew"
        )

        tk.Label(
            self,
            text="Note:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=(0, 10),
            pady=(10, 0)
        )

        self.grade_entry = tk.Entry(
            self,
            state="disabled"
        )
        self.grade_entry.grid(
            row=1,
            column=1,
            sticky="ew",
            pady=(10, 0)
        )

        self.columnconfigure(1, weight=1)

        self.save_result_button = tk.Button(
            self,
            text="Speichern",
            command=self.on_save
        )
        self.save_result_button.grid(
            row=2,
            column=1,
            sticky="e",
            pady=(10, 0)
        )

    def update(
        self,
        exam_result=None,
        is_creating=False
    ):
        self.exam_result = exam_result
        self.is_creating = is_creating

        editor_active = (
            exam_result is not None
            or is_creating
        )

        self.exam_type_combobox.config(
            state="readonly"
            if editor_active
            else "disabled"
        )

        self.grade_entry.config(
            state="normal"
            if editor_active
            else "disabled"
        )

        self.save_result_button.config(
            state="normal"
            if editor_active
            else "disabled"
        )

        self.clear()

        if exam_result is not None:
            self.exam_type_combobox.set(
                exam_result.exam_type.value
            )
            self.grade_entry.insert(
                0,
                str(exam_result.grade)
            )

    def clear(self):
        self.exam_type_combobox.set("")
        self.grade_entry.delete(0, tk.END)

    def focus(self):
        self.exam_type_combobox.focus_set()

    def on_save(self):
        self.on_save_callback(
            self.exam_type_combobox.get(),
            self.grade_entry.get()
        )