from django.contrib.auth.models import User
from django.db import models

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    branch = models.CharField(max_length=10)
    roll = models.CharField(max_length=7)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username

class Grade(models.Model):
    SEM_CHOICES = [
        (1, "Semester 1"),
        (2, "Semester 2"),
        (3, "Semester 3"),
        (4, "Semester 4"),
        (5, "Semester 5"),
        (6, "Semester 6"),
        (7, "Semester 7"),
        (8, "Semester 8"),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.IntegerField(choices=SEM_CHOICES)
    course  = models.CharField(max_length=50)
    marks = models.IntegerField()
    
    def grade(self):
        if self.marks >=90:
            return 'O'
        elif self.marks >=80:
            return 'E'
        elif self.marks >=70:
            return 'A'
        elif self.marks >=60:
            return 'B'
        elif self.marks >=50:
            return 'C'
        elif self.marks >=40:
            return 'D'
        else:
            return 'F'
        
    def __str__(self):
        return f"{self.student} - {self.course} ({self.grade()})"