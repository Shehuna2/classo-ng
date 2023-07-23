from django.urls import path

from . import views

app_name = 'timetable'

urlpatterns = [
    path('add/', views.addCourse, name='add-course'),
    # path('generate/', views.generate_timetable, name='generate-timetable'),
]