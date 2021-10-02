import hashlib
import json
import os
import random
import uuid
from datetime import datetime, timedelta
import time
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import F, Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template import loader
from django.urls import reverse
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt

import mainapp
from mainapp.models import Student, House, Course
from mainapp.tasks import hello_celery
from util.helper import random_string
from celery.signals import task_success, task_postrun


def student_list(request):
    students = [{'id': 1, 'name': "Harry Potter"}, {'id': 2, 'name': "Ronald Weasley"},
                {'id': 3, 'name': "Hermione Granger"}]
    msg = 'Hogwarts student'
    # return render(request, 'student/list.html', {'students': data, 'msg': 'Hogwarts student'})
    return render(request, 'student/list.html', locals())

@csrf_exempt

def add_student(request):  # http://127.0.0.1:8000/student/add?name=Luna%20Lovegood&age=9&house=1

    student = Student()
    #print(request.GET.code)
    student.name = request.GET.get('name', None)  # default value
    student.age = request.GET.get('age', 0)
    student.house = House.objects.get(pk=request.GET.get('house', 0))
    if not all((student.age, student.name, student.house)):  # check valid input
        return HttpResponse('<h3>bad request parameter</h3>', status=400)

    student.save()
    return redirect('/student/list')

def student_list2(request):  # http://127.0.0.1:8000/student/list   student from main urls, list from mainapp urls
    students = Student.objects.all()
    msg = 'Hogwarts student'
    # return render(request, 'student/list.html', {'students': data, 'msg': 'Hogwarts student'})
    return render(request, 'student/list.html', locals())

@cache_page(timeout=5, cache='html_cache',key_prefix='cc')
def student_list3(request):  # http://127.0.0.1:8000/student/list   student from main urls, list from mainapp urls
    page=request.GET.get('page',1)
    students = Student.objects.all()
    msg = 'Hogwarts student'
    paginator = Paginator(students, 2)
    curr_page = paginator.page(page)
    lucky = Student.objects.get(pk=random.randint(1, students.count())).name

    #template = loader.get_template('student/list.html')  # load template
    #html = template.render(context={'msg': 'Hogwarts student', 'students': students})   # render template
    html = loader.render_to_string("list.html", locals(), request)  #  request optional,  use app level template



    return HttpResponse(html, status=200)

def delete_student(request):  # http://127.0.0.1:8000/student/delete?id=15
    id = request.GET.get('id', None)
    if id:
        try:
            student = Student.objects.get(pk=int(id))
            student.delete()
            html = '''
                <p> student with id %s deleted successfully. redirecting to <a href="list">
                    student list</a> in 3 seconds.</p>
                <script> setTimeout(()=>{ window.open('list', target='_self');}, 3000) </script>       
            ''' % id
            return HttpResponse(html)
        except:
            return HttpResponse('student id %s not exist' % id)
    else:
        return HttpResponse('<h3>bad request parameter</h3>', status=400)


def find_student_house(request):  # http://127.0.0.1:8000/student/find_student_house?id=1
    house = request.GET.get('id', None)
    # Student.objects.filter(id=3).update(age=F('age') -1)  # update(age=12)
    # print(Student.objects.filter(Q(house=1) | Q(house=2)).all())
    # print(Student.objects.filter(Q(house=1) | Q(house=2)).values())
    # print([s for s in Student.objects.raw('select id, name,house_id from t_student where age<%s',(11,))])
    # QuerySet.raw() return RawQuerySet  must include id
    # print(Student.objects.extra(where=['house_id=%s'],params=[1]))
    # print(Student.objects.extra(where=['house_id=%s or name like %s','age=%s'], params=[1, 'Mal%', 11]))
    from django.db import connection
    with connection.cursor() as c:
        c.execute('select * from t_student')
        #print([s for s in c.fetchall()])

    #print(Student.objects.get(pk=6).house.name)
    #print(House.objects.get(pk=1).student_set.all())
    #Student.objects.get(pk=5).courses.add(Course.objects.get(pk=2))
    #print(Student.objects.get(pk=5).courses.all())
    #Course.objects.get(pk=2).students.remove(Student.objects.get(pk=5))
    #print(Course.objects.get(pk=2).students.all())
    # print(request.path) # /student/find_student_house

    if id:
        try:
            house = int(house)
            students = Student.objects.filter(house__exact=1).order_by('-id', 'age')
            #print(students)
            # if students.objects.get(3).first().intro=='':
            #    students.objects.get(3).first()
            #print([s.name for s in students])
            request.session['students'] = ([s.name for s in students])
            return render(request, 'list.html', locals())  # from app level templates
        except:
            return HttpResponse('house id %s not exist' % id)
    else:
        return HttpResponse('<h3>bad request parameter</h3>', status=400)

def detail(request, id):  # retrieve url path parameter (not request.get)
    if request.method == 'GET':
        student = Student.objects.get(pk=id)
        url = reverse('hogwarts:info', args=(id,))
        host = request.get_host()
        path = student.logo.url.split('/')[-1]
        pic_src = '../media/storage/'+path
        #print(url)
    return render(request, 'detail.html', locals())

def images(request, name):
    if name:
        path = os.path.join(os.getcwd(), 'media','storage', name)

        with open(path, 'rb') as f:
            img = f.read()
        resp = HttpResponse(content=img) # , content_type='image/jpeg'
        resp['Content-Type'] = 'image/jpeg'
        resp.setdefault('Content-Length', len(img))  # update Content-Length in response headers
                                # (chrome browser, network tab, click on img, under headers tab)
    token = uuid.uuid4().hex
    resp.set_cookie('token', token, expires=datetime.now()+timedelta(minutes=2))
    # (chrome browser, network tab, click on img, under Cookie tab)
    #resp.delete_cookie('token')  # delete cookie

    return resp

def verification_code(request):
    img = Image.new('RGB',(80,40), (255,255,200)) # mode(RGB,ARGB), (width,height), bg (rgb)color. draw on white sheet
    draw = ImageDraw.Draw(img, 'RGB')  # image object, mode
    font_color = (0, 20, 100)
    font = ImageFont.truetype('static/fonts/Pacifico.ttf', size=20)
    valid_code = random_string(5)
    request.session['code'] = valid_code
    draw.text((5,-5), valid_code, font=font, fill=font_color)  # start (x,y) coordinates, text
    for x in range(200):
        x, y = random.randint(0,80), random.randint(0,40)
        r, g, b = random.randint(0,255),random.randint(0,255),random.randint(0,255),
        draw.point((x, y), (r,g,b))
    buffer = BytesIO()
    img.save(buffer, 'png')  # write img
    return HttpResponse(content=buffer.getvalue(), content_type='image/png')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', locals())
    def post(self,request):
        stu_name = request.POST.get('name')
        pwd = request.POST.get('password')
        if stu_name and pwd:
            pwd = hashlib.sha224(pwd.encode('utf-8')).hexdigest()
            student = Student.objects.filter(name=stu_name).first()
            #print(student)
            if student and student.password == pwd:
                request.session['student'] = json.dumps({'user': student.name, 'id': student.id})
                request.session.set_expiry(1000)  # 100 seconds
                #print(request.session.get('student'))
                #url =reverse('hogwarts:info', args=(student.id,))
                url = '/student/detail2'
                #resp = render(request, 'detail.html', locals())
                resp = redirect(url, locals())
                #request.session.clear()
                #if not request.COOKIES.get('token'):
                #    resp.set_cookie(key='token', value=uuid.uuid4().hex)
                if not cache.has_key('student'):
                    cache.add('student', json.dumps({'user': student.name, 'id': student.id}), timeout=1000)

                #print(cache.get('student'))

                return resp
            else:
                return redirect('/student/login')
        else:
            return redirect('/student/login')
    def put(self,request):
        return HttpResponse('Put Request')
    def delete(self,request):
        return HttpResponse('Delete Request')

def detail2(request):  # retrieve url path parameter (not request.get)
    info = request.session.get('student')  # {"user": "Harry Potter", "id": 1}
    info2 = request.headers
    mainapp.codeSignal.send('api', path=request.path, memo='detail is here %s' % info)
    # sender name, keys values in side param list to send
    if info:
        info = eval(info)
        id = info.get('id')
        student = Student.objects.get(pk=id)
        msg = 'Welcome %s' % student.name
        url = reverse('hogwarts:info', args=(id,))
        host = request.get_host()
        if student.logo:
            path = student.logo.url.split('/')[-1]
            pic_src = '../media/storage/'+path

        return render(request, 'detail.html', locals())

    else:
        return redirect('/student/list')


