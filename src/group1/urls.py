from django.urls import path
from .views import exam_list, take_exam, exam_result
from django.conf import settings
from django.conf.urls.static import static

# add three url and static audio files
urlpatterns = [
    path('exams/', exam_list, name='exam_list'),
    path('exams/<int:exam_id>/', take_exam, name='take_exam'),
    path('exams/<int:exam_id>/result/', exam_result, name='exam_result'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
