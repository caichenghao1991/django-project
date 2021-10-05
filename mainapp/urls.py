from django.conf.urls import url
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from mainapp.views import student_list, student_list2, add_student, delete_student, find_student_house, student_list3, \
    detail, images, verification_code, LoginView, detail2, student_list_api, StudentAPIView, change_image_size, \
    send_student_email

app_name = 'mainapp'



urlpatterns = [
    path('list/', student_list3),
    url(r'^list2$', student_list2),  # path implementation in django 1.x
    path('add', add_student),
    path('delete', delete_student),
    path('find_student_house', find_student_house),
    path('detail/<int:id>', detail, name='info'),

    path('images/<name>', images, name='img'),
    path('change_image_size/<id>/<size>', change_image_size),
    path('verification/', verification_code),
    path('login',LoginView.as_view(), name='login'),
    path('detail2', detail2),
    path('list_api', student_list_api,name='api'),
    path('student_api/<id>', StudentAPIView.as_view()),
    path('send_email/<code>', send_student_email),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
