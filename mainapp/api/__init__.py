from rest_framework import routers

from mainapp.api.students_api import StudentAPIView, HouseAPIView

api_router = routers.DefaultRouter()
api_router.register('students', StudentAPIView)
api_router.register('houses', HouseAPIView)