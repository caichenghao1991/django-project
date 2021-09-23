from django.urls import path
from mainapp.views import student_list, student_list2, add_student, delete_student

urlpatterns = [
    path('list', student_list2),
    path('add', add_student),
    path('delete', delete_student)
]
