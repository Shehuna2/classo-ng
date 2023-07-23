from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('home/', views.home, name='home'), 
    path('home/<str:section_name>/', views.home, name='home-section'), 
    path('topic/<int:id>/', views.topicDetails, name='topic-details'), 
    path('add_topic/', views.addTopic, name='add-topic'),

    path('curriculum/', views.curriculumList, name='curriculum-list'),
    path('curriculum/syllabus/<str:section_name>/', views.curriculumList, name='curriculum-section'),
    path('curriculum/details/<int:id>/', views.curriculumDetails, name='curriculum-details'), 

    path('exams/', views.examList, name='exams-list'),
    path('exams/<str:section_name>/', views.examList, name='exams-section'),
    path('exam/<int:id>/', views.examDetails, name='exam-details'), 
    path('add_exam/', views.addExam, name='add-exam'),

    path('contact/', views.contactUs, name='contact-us')
]