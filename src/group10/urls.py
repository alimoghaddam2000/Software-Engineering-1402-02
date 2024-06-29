from django.urls import path
from . import views

urlpatterns = [
    path('index_page', views.index_page, name='index_page'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('courses', views.courses, name='courses'),
    path('course/<id>', views.course_page, name='course_page'),
    path('create_course', views.create_course, name='create_course'),
    path('add_video/<id>', views.add_video, name='add_video'),
    path('course-poster/<course_id>/', views.get_course_poster, name='course_poster'),
    path('create_exam/<course_id>', views.create_exam, name='create_exam'),
    path('exam/<exam_id>', views.exam_page, name='exam_page'),
    path('add-question/<exam_id>/', views.add_question, name='add_question'),

]
