from django.conf.urls import url
from django.urls import path
from mainapp.views import student_list, student_list2, add_student, delete_student, find_student_house, student_list3

urlpatterns = [
    path('list', student_list3),
    url(r'^list2$', student_list2),  # path implementation in django 1.x
    path('add', add_student),
    path('delete', delete_student),
    path('find_student_house', find_student_house)
]
