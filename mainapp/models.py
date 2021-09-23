from django.db import models


# Create your models here.
class House(models.Model):
    name = models.CharField(max_length=30, verbose_name='House Name')

    def __str__(self):  # add this so in the admin page, will show student name instead of object
        return self.name
    class Meta:
        db_table = 't_house'
        verbose_name = 'house'  # name inside admin page

class Student(models.Model):
    name = models.CharField(max_length=50, verbose_name='Student Name')  # verbose name for admin page
    age = models.IntegerField(default=0, blank=True, null=True)
    # admin page(blank=True) / database (null=True) add studentcan be empty
    #house = models.IntegerField(default=0, blank=True, null=True)
    house = models.ForeignKey(House, on_delete=models.SET_NULL, null=True, db_index=True)  # CASCADE create index
    #id = models.UUIDField(primary_key=True, unique=True)
    #gender = models.IntegerField(choices=((0, 'male'),(1, 'female')), db_column='sex')
        # save 0/1 column name sex, but display male/female in admin page
    #join_date = models.DateField(auto_now_add=True)  # add create time as now
    '''def __init__(self, name: str, age: int, house: int):
        self.name = name
        self.age = age
        self.house = house
    '''

    def __str__(self):  # add this so in the admin page, will show student name instead of object
        return self.name

    class Meta:
        db_table = 't_student'
        verbose_name = 'student'  # name inside admin page
        verbose_name_plural = 'student'  # set plural name (default add s)
        ordering = ['age']  # default ascending, ['-age'] descending
        unique_together = ('name','age','house')