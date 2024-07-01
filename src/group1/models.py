from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Exam(models.Model):
    #define difficalty level
    DIFFICULTY_LEVEL_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_LEVEL_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class AudioFile(models.Model):
    exam = models.ForeignKey(Exam, related_name='audio_files', on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to='')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Audio for {self.exam.title}'

class Question(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('MC', 'Multiple Choice'),
        ('TX', 'Text Answer'),
    ]

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question_text = models.TextField()
    question_type = models.CharField(max_length=2, choices=QUESTION_TYPE_CHOICES)
    options = models.JSONField(blank=True, null=True)
    correct_answer = models.TextField()

    def __str__(self):
        return self.question_text
#saves student exam records 
class StudentExamRecord(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField() 
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Student {self.student.username} - Exam {self.exam.title}'
