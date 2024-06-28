from django.contrib import admin
from .models import Category, Exam, AudioFile, Question, StudentExamRecord

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'category', 'date_created')
    list_filter = ('difficulty', 'category')
    search_fields = ('title', 'description')

@admin.register(AudioFile)
class AudioFileAdmin(admin.ModelAdmin):
    list_display = ('exam', 'description', 'audio_file')
    search_fields = ('exam__title', 'description')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('exam', 'question_text', 'question_type')
    list_filter = ('question_type', 'exam')
    search_fields = ('question_text',)

@admin.register(StudentExamRecord)
class StudentExamRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'question', 'answer', 'date_taken')
    list_filter = ('exam', 'question', 'date_taken')
    search_fields = ('student__username', 'exam__title', 'question__question_text', 'answer')
