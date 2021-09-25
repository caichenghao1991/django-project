from django.contrib import admin
from mainapp.models import House, Student
# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    # change the display of student in the admin page
    list_display = ('id', 'name')
    list_per_page = 10  # count of student per page in the admin page
    list_filter = ('age', 'house')  # admin page add option filter student by age, or by house
    search_fields = ('id', 'name') # admin page search student by id or name
    list_display = ('id', 'name', 'age', 'house_str', 'grade', 'logo', 'logo_width','logo_height','intro')
class HouseAdmin(admin.ModelAdmin):
    # change the display of student in the admin page
    list_display = ('id', 'name')
    # fields = ('name',)  # specify the admin page field required during add, can exclude some field

admin.site.register(House, HouseAdmin)
admin.site.register(Student, StudentAdmin)