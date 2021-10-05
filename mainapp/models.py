import hashlib
import re

import time
from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.
class House(models.Model):
    name = models.CharField(max_length=30, verbose_name='House Name')
    # default house.student_set.all() get all student in current house object, unless use related_name in many side

    def __str__(self):  # add this so in the admin page, will show student name instead of object
        return self.name

    class Meta:
        db_table = 't_house'
        verbose_name = 'house'  # name inside admin page

class StudentValidator:
    @classmethod
    def valid_age(cls, value):
        if not re.match(r'\d{2}', str(value)):  # int must convert to string
            raise ValidationError('Incorrect age for Hogwarts')
        return True

class Student(models.Model):
    name = models.CharField(max_length=50, verbose_name='Student Name')  # verbose name for admin page
    password = models.CharField(max_length=100, verbose_name='Password', null=True, blank=True)
    age = models.IntegerField(default=0, blank=True, null=True, validators=[StudentValidator.valid_age])
    # admin page(blank=True) / database (null=True) add studentcan be empty
    # house = models.IntegerField(default=0, blank=True, null=True)
    house = models.ForeignKey(House, on_delete=models.SET_NULL, null=True, db_index=True, related_name='students')
        # CASCADE create index, change access in house table from student_set to students
    # id = models.UUIDField(primary_key=True, unique=True)
    # gender = models.IntegerField(choices=((0, 'male'),(1, 'female')), db_column='sex')
    # save 0/1 column name sex, but display male/female in admin page
    join_date = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Join Date')  # add create time as now

    logo = models.ImageField(upload_to='storage', width_field='logo_width', height_field='logo_height', blank=True)
    logo_width = models.IntegerField(null=True, blank=True)
    logo_height = models.IntegerField(null=True, blank=True)
    intro = models.TextField(blank=True, null=True)

    '''def __init__(self, name: str, age: int, house: int):
        self.name = name
        self.age = age
        self.house = house
    '''

    @property
    def grade(self):
        return int(time.strftime('%Y')) - int(self.join_date.strftime('%Y')) + 1



    def __str__(self):  # add this so in the admin page, will show student name instead of object
        return self.name

    def save(self, *args, **kwargs):
        self.password = hashlib.sha224(self.password.encode('utf-8')).hexdigest()
        super(Student, self).save(*args, **kwargs)

    '''
    # if use UUIDField as primary key 
    def save(self,  force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.id:
            self.id = uuid.uuid4().hex
        super.save()
    '''

    class Meta:
        db_table = 't_student'
        verbose_name = 'student'  # name inside admin page
        verbose_name_plural = 'student'  # set plural name (default add s)
        ordering = ['age']  # default ascending, ['-age'] descending
        unique_together = ('name', 'age', 'house')


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name='Course Name')
    grade = models.IntegerField(verbose_name='Year taking this course')
    students = models.ManyToManyField(Student, db_table='t_student_course', related_name='courses',
                                      verbose_name='Students took this course')

    def __str__(self):  # add this so in the admin page, will show student name instead of object
        return self.name
    # create t_student_course to track many to many relation, use courses instead of student_set for reverse inference
    class Meta:
        db_table = 't_course'
        verbose_name = 'course'  # name inside admin page
        verbose_name_plural = 'course'  # set plural name (default add s)

