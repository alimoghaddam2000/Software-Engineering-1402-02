from django.urls import path
from .views import exam_list, take_exam, exam_result

urlpatterns = [
    path('exams/', exam_list, name='exam_list'),
    path('exams/<int:exam_id>/', take_exam, name='take_exam'),
    path('exams/<int:exam_id>/result/', exam_result, name='exam_result'),
]
