from django.db.models import F, Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.

from mainapp.models import Student, House


def student_list(request):
    students = [{'id': 1, 'name': "Harry Potter"}, {'id': 2, 'name': "Ronald Weasley"},
                {'id': 3, 'name': "Hermione Granger"}]
    msg = 'Hogwarts student'
    # return render(request, 'student/list.html', {'students': data, 'msg': 'Hogwarts student'})
    return render(request, 'student/list.html', locals())


def add_student(request):  # http://127.0.0.1:8000/student/add?name=Luna%20Lovegood&age=9&house=0

    student = Student()
    student.name = request.GET.get('name', None)  # default value
    student.age = request.GET.get('age', 0)
    student.house = request.GET.get('house', 0)
    if not all((student.age, student.name, student.house)):  # check valid input
        return HttpResponse('<h3>bad request parameter</h3>', status=400)

    student.save()
    return redirect('/student/list')


def student_list2(request):  # http://127.0.0.1:8000/student/list   student from main urls, list from mainapp urls
    students = Student.objects.all()
    msg = 'Hogwarts student'
    # return render(request, 'student/list.html', {'students': data, 'msg': 'Hogwarts student'})
    return render(request, 'student/list.html', locals())


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
    #Student.objects.filter(id=3).update(age=F('age') -1)  # update(age=12)
    #print(Student.objects.filter(Q(house=1) | Q(house=2)).all())
    #print(Student.objects.filter(Q(house=1) | Q(house=2)).values())
    #print([s for s in Student.objects.raw('select id, name,house_id from t_student where age<%s',(11,))])
        # QuerySet.raw() return RawQuerySet  must include id
    #print(Student.objects.extra(where=['house_id=%s'],params=[1]))
    #print(Student.objects.extra(where=['house_id=%s or name like %s','age=%s'], params=[1, 'Mal%', 11]))
    from django.db import connection
    with connection.cursor() as c:
        c.execute('select * from t_student')
        print([s for s in c.fetchall()])

    print(Student.objects.get(pk=6).house.name)
    print(House.objects.get(pk=1).student_set.all())

    if id:
        try:
            house = int(house)
            students = Student.objects.filter(house__exact=house).order_by('-id', 'age')



            #if students.objects.get(3).first().intro=='':
            #    students.objects.get(3).first()

            return render(request, 'student/list.html', locals())
        except:
            return HttpResponse('house id %s not exist' % id)
    else:
        return HttpResponse('<h3>bad request parameter</h3>', status=400)
