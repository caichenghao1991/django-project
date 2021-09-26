from django.contrib import admin
from mainapp.models import House, Student, Course


# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    # change the display of student in the admin page
    list_display = ('id', 'name')
    list_per_page = 10  # count of student per page in the admin page
    list_filter = ('age', 'house')  # admin page add option filter student by age, or by house
    search_fields = ('id', 'name')  # admin page search student by id or name
    list_display = ('id', 'name', 'age', 'house_str', 'grade', 'logo', 'logo_width', 'logo_height', 'intro')

    def house_str(self, obj):
        return obj.house.name

    house_str.short_description = 'house name'  # change admin display name

class HouseAdmin(admin.ModelAdmin):
    # change the display of student in the admin page
    list_display = ('id', 'name')
    # fields = ('name',)  # specify the admin page field required during add, can exclude some field

class CourseAdmin(admin.ModelAdmin):
    # change the display of student in the admin page
    list_display = ('id', 'name', 'grade')

admin.site.register(House, HouseAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
