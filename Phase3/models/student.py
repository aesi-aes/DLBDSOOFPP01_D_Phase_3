from dataclasses import dataclass

# Student
# TODO: wirklich sinnvolle Klasse? checken - momentan eigentlich total sinnlos ohne direkten Zusammenhang mit Kursen.
@dataclass
class Student:
    student_number: int
    current_semester: int