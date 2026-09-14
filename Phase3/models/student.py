from dataclasses import dataclass

from models.degree_program import DegreeProgram


# Student hält Referenz auf Studienfach
# TODO: wirklich sinnvolle Klasse? checken - momentan eigentlich total sinnlos ohne direkten Zusammenhang mit Kursen.
@dataclass
class Student:
    student_number: int
    current_semester: int
    degree_program : DegreeProgram