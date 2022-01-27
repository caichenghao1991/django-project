'''
    Django is a high-level python web framework encourage rapid development and clean pragmatic design, not a webserver
    Django too heavy for handling api (mainly use flask/tornado), django is good for backend managing
        system
    django-admin help startproject   check helper function
    django-admin startproject djangoSample  # projectName
        # django-admin startproject django-project ./  # no extra layer directory if same project name and already
                # created folder with same name
        djangoSample
            |-- djangoSample   # main project directory
                |-- settings.py  # settings file, database config,  app registry, template config
                |-- urls.py   # main router
                |-- wsgi.py   # Django implementation of wsgi script
                |-- __init__.py
            |-- mainapp   # app module(main)
                |-- __init__.py
                |-- admin.py      # background manager config script
                |-- models.py     # data model declaration script
                |-- views.py      # current app view control function and class
                |-- urls.py       # current app child routing
                |-- tests.py      # unit test for current app
                |-- apps.py       # declare basic information of current app

    ./manage.py shell             # test some code with django environment

    django-admin startapp mainapp
    python manage.py startapp mainapp
        # one django project contain many app (module), register app into the main project settings.py

    django-admin startapp mainapp  # this will create a folder named mainapp, with empty structure files
        # add main app in main project(djangoSample)
        settings.py: INSTALLED_APPS   add 'mainapp'
             TEMPLATES   'DIRS': [os.path.join(BASE_DIR, 'templates')],  # this is for all app templates location
             LANGUAGE_CODE = 'en-us'  # change language
             TIME_ZONE = 'GMT'  # change time zone

             # model use upload file/image url and dir
             MEDIA_URL = '/media/'
             MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
             STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
        urls.py    # main urls
        def index(request: HttpRequest):    # views controller, must have http request param from browser
            return HttpResponse('<h1>hi, Django</h1>'.encode('utf-8'))   # or string

        urlpatterns = [
            path('admin/', admin.site.urls),
            path('', index)   # not /  '' for index page
            path('user/', include('mainapp.urls'))  # add urls for mainapp and other app. config child router
        ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   # add static if need add file/image data
         # path('url', view_function, name=None)
         # path('url/', include('app_name.urls', namespace='hogwarts'))    # include child url path

        mainapp urls.py  # each app urls
        from mainapp.views import student_list2
        app_name = 'mainapp'   # for Reversing namespaced URLs
        urlpatterns = [path('list', student_list2, name='list'),
                    path('delete/<id>/<int: sid>', student_delete, name='delete'),
                    # parameter type: str, int, slug(ASCII letter,digit,_,-), uuid  (uuid.uuid4())
                    re_path(r'^delete/(\w+)/(?P<s_id>\d+)$', student_delete), # same as url in django 1.x

                    url(r'^list2$', student_list2),  # path implementation in django 1.x
                    url(r'^delete/(\w+)/(?P<s_id>\d+)$', student_delete)]  # pass variable into view function, need ()
        # def student_delete(request, id, s_id):  # here id, s_id is passed from url. match by left to right, or keyword

        # path('url', view_function, name=None)
        # name and namespace in the path/include are used for Reversing namespaced URLs  (get url from path logic)
    Reversing namespaced URLs: used in view and HTML template for getting the url path of request
    urls.py    # main urls
        urlpatterns = [path('url/', include('app_name.urls', namespace='hogwarts'))
    mainapp urls.py mainapp urls.py
        app_name='mainapp'  # need add app name if main url have namespace
        urlpatterns = [path('detail/<int:id>', detail, name='info')

    html:
       <a href="{% url 'hogwarts:info' stu.id %}">More info</a>
       <a href="{% url 'hogwarts:info' id='stu.id' %}">More info</a> #  specify parameter
        # can have multiple parameter separated by space

    views:
        sid = id
        url = reverse('hogwarts:info', args=(sid,))  # pass parameter base on location
        url = reverse('hogwarts:info', kwargs=dict(id=sid, house='Gryffindor'))  # pass dict parameter
        return redirect(url)   # return HttpResponseRedirect(url)

    python manage.py runserver  # start server   python manage.py runserver 127.0.0.1:7000  # 0.0.0.0:5000 any ip
        python manage.py runserver 8000  # only specify port
    before yse orm model, if using sqlite3. need to generate migrate file and migrate to generate tables. Otherwise,
        there will be no data in the database

    python manage.py makemigrations  # generate migration file, do not delete migration file
    python manage.py migrate   # migrate database
        # python manage.py migrate mainapp 1   # migrate only specified app and provide migrate number
    python manage.py showmigrations    [x]  migrated  [ ]  not yet migrated

    python manage.py shell   # open shell
        >>> from mainapp.models import Student

    # Create your models here.
    from django.db import models
    class Student(models.Model):  # default create autoincrement primary key id
        name = models.CharField(max_length=50, verbose_name='Student Name')  # verbose name for admin page
        age = models.IntegerField(default=0)   # if empty no default will raise error
        house = models.IntegerField(default=0, blank=True, null=True)
            # admin page(blank=True) / database (null=True) add student can be empty
        #id = models.UUIDField(primary_key=True, unique=True)
        #gender = models.IntegerField(choices=((0, 'male'),(1, 'female')), db_column='sex')
        # save 0/1 column name sex, but display male/female in admin page
        join_date = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Join Date')
            # add create time as now, won't show up in admin add field
        logo = models.ImageField(upload_to='images', width_field='logo_width', height_field='logo_height', blank=True)
            # width_field, height_field default to picture original size, can't be changed
            # upload_to  will create a new folder under MEDIA_ROOT  # http://127.0.0.1:8000/media/storage/hp.jpg
        logo_width = models.IntegerField(null=True, blank=True)
        logo_height = models.IntegerField(null=True,blank=True)
        intro = models.TextField(blank=True, null=True)

        def __str__(self):
            # add this so in the admin page, will show student name instead of object
            return self.name

        # if use UUIDField as primary key
        def save(self,  force_insert=False, force_update=False, using=None, update_fields=None):
            if not self.id:
                self.id = uuid.uuid4().hex
            if len(self.password)<30:
                self.password = make_password(self.password)
            super.save()

        def save(self, *args, **kwargs):
            self.password = hashlib.sha224(self.password.encode('utf-8')).hexdigest()
            super(Student, self).save(*args, **kwargs)

        class Meta:
            db_table = 't_student'  # set projected table name
            db_table = 't_student'
            verbose_name = 'student'  # name inside admin page
            verbose_name_plural = 'student'  # set plural name (default add s)
            ordering = ['age']  # default ascending, ['-age'] descending
            unique_together = ('name', 'age', 'house')

    views.py
    def student_list2(request):  # http://127.0.0.1:8000/student/list
        request.method == 'GET':
        students = Student.objects.all()  # get all objects from t_student table
        student = Student.objects.get(pk=1)  # search object by primary key=1   or get(id=1)
            # get(name='Harry')  exception if more than one item, or no item exist
        Student.objects.get(pk=1).update(name='Jr'+F('name'))
        student.delete()   # delete object in database
        msg = 'Hogwarts student'
        request.session['students'] = ([s.name for s in students])  # put json serializable object inside session
        #return render(request, 'student/list.html', {'students': data, 'msg': 'Hogwarts student'})
        return render(request, 'student/list.html', locals())
    def add_student(request):  # http://127.0.0.1:8000/student/add?name=Luna%20Lovegood&age=9&house=0
        student = Student()
        student.name = request.GET.get('name', None)  # default value
        student.age = request.GET.get('age', 0)
        student.house = request.GET.get('house', 0)
        student.hobby = request.GET.getlist('hobby')  # get list with same key, used for checkboxes
        file = request.FILES.get('img1')  # html name='img1'  get files in form
            file.name, content_type, size, charset
        student.save()  # save/update object
        return redirect('/student/list')   # use redirect when path already defined in the view
    s1=Student.objects.create(name='Harry Potter', age=11, house=House.objects.get(1))
        # create object s1 add in db
    s1.name='Daniel'
    Student.objects.bulk_create([s1,s2]) # create and save multiple entries

    import sqlite3
    sqlite is a small database, mainly used for browser, mobile device. It support SQL grammar, but no data type.
    It will determine the data type by coding language grammar and data type

    conn = sqlite3.connect('student.sqlite3')  # automatically create database if not exist
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE student(id Integer PRIMARY KEY, name, age, house)")  # primary key auto increment
    cursor.execute("INSERT INTO student(name, age, house) values('Harry Potter', 10, 'Gryffindor')")
    cursor.execute("SELECT * FROM student")
    for row in cursor.fetchall():
        print(row)


    python manage.py createsuperuser
        # type username, email, password
        # http://127.0.0.1:8000/admin   login amin page  add/delete/update user/role
    admin.py
    class StudentAdmin(admin.ModelAdmin):
        # change the display of student in the admin page
        list_display = ('id','name')
        list_per_page = 10  # count of student per page in the admin page
        list_filter = ('age','house')  # admin page add option filter student by age, or by house
        search_fields = ('id', 'name')  # admin page search student by id or name
        # fields = ('name',)  # specify the admin page field required during add, can exclude some field
    admin.site.register(Student, StudentAdmin))  # admin.site.register(Student)
        # or add @admin.register(Student) in front of class StudentAdmin(admin.ModelAdmin):
    data type
    CharField: string      IntegerField: int    BooleanFeild: 0/1 in database     NullBooleanField: nullable boolean
    AutoField: int autoincrement need add primary-key=True, auto_create # create column automatically
    FloatField (max_digits, decimal_places)     TextField     UUIDField: string type
    ImageField (path  upload_to="", images,width_field, height_feild)   DateField (auto_now: update time,
    auto_now_add: create time, YYYY-MM-DD. auto_now and auto_now_add can't use together)
    DateTimeField (datetime.datetime, YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ])          TimeField

    constraint: max_length, default, unique, primary_key, null, blank, db_index, db_column, verbose_name, choices

    meta: db_table (declare table name), ordering, verbose_name, verbose_name_plural, unique_together,
        abstract(don't create table)

    template html same as flask
    {% for item in items %} {% endfor %}
    {% if items>0 %} {% endif %}
    {{ variable }}
    {% block name %} {% endblock %}  # name is the block name
    {% extends "base.html" %}
    {% include 'base_js.html' %}  # include page can't modify
    return render(request, 'student/list.html', locals())

    type class which create the model class will default create a django.db.Manager class object assign to objects.
        Manager is subclass of QuerySet class (mode, db, query, filter, fields, lookup, iterable)
        objects must be a Manager class object

    objects functions:
        QuerySet: filter, exclude
            condition: gt, lt, gte, lte, exact, iexact(ignore case), contains, icontains, in, isnull, isnotnull
        join_date__year__gt=2021  # year, month, dat, hour, minute, second
        students = Student.objects.filter(age__gt=10,name__contains='Har').exclude(age__gt=20).all()
            .order_by('-id', 'age')
        # can chain filters and exclude  (10,20], filter can have multiple conditions
        Student.objects.filter(id__range=(1,100)).only('name','age')   # use only to get specified column
            # defer('birth')  # get all columns except 'birth'


        Single Object: get() last()  first()  # return an object
        Other: exists():boolean check result exists    count()      order_by()
             values_list()   values():  return queryset, but iterative item is dict
             values('id','name')  # return queryset of dict item only contains specified column
             all()   return queryset, but iterative item is object

        use built in function instead of mix of python function, ORM data transfer through TCP from database, do all
            calculation at database side to minimize the data transferred

        Aggregate
        from django.db.models import Count, Avg, Min, Max, Sum
        aggregate return dict
        Student.objects.aggregate(Count('age'), max=Max('age'))  # add var=Max() change display name on page
            # {'age_count':10, 'max':12}
        Student.objects.annotate(Count('courses')).filter(age__gt=1)   # return student queryset with extra
            # courses_count  column

        update on QuerySet object
        Student.objects.filter(id__gte=3).update(intro='Hi')
        Student.objects.filter(age=10).update(age=F('age') -1)   # multiple update

        create
        Student.objects.create(name="Luna Lovegood", age=10, house=1)
        stu, created = Student.objects.get_or_create(name="Luna Lovegood", age=10, house=1)
            # get object if exist otherwise create new object     # return object and boolean value of whether created
        bulk_create(),  update_or_create()

        delete
        work on object and queryset
        Student.objects.get(pk=1).delete()   # delete one object
        Student.objects.filter(age=10).delete()   # delete queryset

        logic operation: use Q   & | ~
        from django.db.models import Q
        Student.objects.filter(Q(house=1)|Q(house=2))

        native sql
        QuerySet.raw() # return rawQuerySet object, must search the column name inside database, iterative model objects
        QuerySet.extra() # return QuerySet object, iterative model objects, must search the column name inside database
        django.db.connection # connection get cursor, execute() fetchall() rowcount() functions

        [s for s in Student.objects.raw('select id, name,house_id from t_student where age<11')] # list of objects
            ('select id, name,house_id from t_student where age<%s',(11,))] # can use %s list or tuple
            ('select id, name,house_id from t_student where age< %(age)s',{'age':11})]  % dict

        Student.objects.extra(where=['house_id=%s'],params=[1])
        Student.objects.extra(where=['house_id=%s or name like %s','age=%s'], params=[1, 'Mal%', 11])

        from django.db import connection
        with connection.cursor() as c:
            c.execute('select * from t_student')
            print([s for s in c.fetchall()])
            c.execute('update t_student set age =11 where id=1')
            print(c.rowcount)
            connection.commit()


    custom model manager and parent class extension
        class BaseModel(models.Model):
            name = models.CharField(max_length=50)
            class Meta:
                abstract = True
        class Student(BaseModel):  # extend BaseModel,
            class StudentManager(models.Manager):  # custom queryset, do pre-filter job
                def get_queryset(self):
                    return super().get_queryset().filter(~Q(house_id=''))
                        # filter out student don't belong to any house
                def update(self, **kwargs):
                    password = kwargs.get('password',None)
                    if password and len(password) < 30:
                        kwargs['password']=make_password(pass_word)
                    return super().update(**kwargs)
            objects=StudentManager()
                # objects=models.Manager()  default implicit call default manager to manage Student.objects
        Students.objects.get(pk=1).update(name='Harry')   # call custom update in StudentManager

    Relation
        one to one:
        class Person(models.Model):    # subordinate table
            student = models.OneToOneField(Student, on_delete=models.CASCADE)
                # add to_field=id   if default key is not primary key
            id_number = models.IntegerField(default=0)
        student = Person.objects.filter(id_number=0001).first().student  # retrieve main table object
        Student.objects.get(pk=1).person.id_number  # main table get subordinate table (lower case)

        # use @property or @cached_property  for distributed system
            @cached_property
            def Person(self):
                if not hasattr(self,'_person'):    # lazy loading
                    self._person = Person.objects.get(id=self.id)
                return self._person   # for one to one relationship

        # many to one
        Student.py  (many side)
        house = models.ForeignKey(House, on_delete=models.SET_NULL, null=True, db_index=True)

        print(Student.objects.get(pk=6).house.name) # retrieve main table object
        print(House.objects.get(pk=1).student_set.all())  # retrieve subordinate table QuerySet
            # main_object.subclassname_set    (lowercase)  can use related_name to change reverse inference name

        # for distributed system many side add
        @cached_property
        def Student(self):
            if not hasattr(self,'_student'):    # lazy loading
                self._student = Person.objects.filter(house_id=self.id)
            return self._student   # for one to many relationship

        # many to many
        class Course:   # create many to many relation, need create extra table compare to many to one
            students = models.ManyToManyField(Student, db_table='t_student_course', related_name='courses',
                verbose_name='Students took this course')
                # create 3rd table for tracking many to many relationship
                # default reverse inference name is course_set, change to courses. return queryset

            #use string if course class declared ahead of student class, or self reference
            students = models.ManyToManyField('Student', db_table='t_student_course', related_name='courses',
                verbose_name='Students took this course')
                # self reference use string class name or 'self'

        # many to many relationship can add/ remove on both table using reference and inverse reference
        Student.objects.get(pk=5).courses.add(Course.objects.get(pk=2))
        print(Student.objects.get(pk=5).courses.all())
        Course.objects.get(pk=2).students.remove(Student.objects.get(pk=5))
        print(Course.objects.get(pk=2).students.all())

        # for distributed system create extra table save both tables' id column

    MTV
        V (view functions) can render multiple T (template). One T can be used by multiple V.
        load template: use django.template.loader object
        template = loader.get_template('index.html')
        html = template.render(context)  # context is dict for loading data
        # or use   html = loader.render_to_string("index.html",context)
        # compare to django.shortcuts. render function, can put the returned object into cache to avoid render again

        use . to access attributes and functions of object, dictionary.key access value, list.index access value
        function can't parse parameter
        {% if students %}
            {% for stu in students %}   # {% for k, v in dic.items %}
                {% if forloop.counter0 == 1 %}    # forloop.counter0 start index 0, counter start 1
                                              # revcounter  revcounter0  first  last       cycle  empty
                    <p>say hi {{ stu.name.upper }}</p>
                {% elif forloop.counter0 == 2 %}
                    <p>say hi {{ stu.name.lower }}</p>
                {% else %}
                {% endif %}
                <li class="{% cycle 'even' '' %}">{{ stu.id }} {{ stu.name }} {{ stu.house.name }}</li>
                    # cycle makes value each time next item
                {% empty %}   # students not none but no items inside
                    <li> no data </li>
            {% endfor %}
        {% endif %}
        {% if %}  and  or  not  in  ==  !=  >  <
        {% ifequal value1 value2 %} xxx {% endifequal %}
        {% ifnotequal value1 value2 %} xxx {% endifnotequal %}

        {% students.2.age|add:5 }}
        {% withratio price 10 3 %}  # price * 3/10
        {% if num|divisibleby:2 %} # check divisibility
          <li {% if forloop.counter0|divisibleby:2 %} class="even" {% endif %}> {{ stu.id }} {{ stu.name }}  </li>

        {% students.2.name|lower }}  upper  capfirst  value|cut:arg (remove all arg in value)
        join:',' (link iterable with character)
        {% students.2.name|default:'None' }}  {% students.2.join_date| date:'Y-m-d H:i:s a' }}

        {{ students.2.house.name}}
        {% include 'base_js.html' %}  # include page can't modify
        {# #} single line comment   {% comment %} multiline comment {% endcomment %}
        <!-- --> html comment will keep the code
`
        {% autoescape off%} {{ body }}{% endautoescape %}  # will allow escaping in variable (> change to &gt)
            # on or {{ code|escape }} will show the code, off or  {{ code|safe }} will show the transferred html
            # better use code text instead of html render, to prevent injection

        filesizeformat, {{dic|dictsort:"name"}} (sort via key), dictsortreversed, {{value|length}} (length of value)
        {{ dic|first}} (first item in dic), last, {{value|floatformat:3}} (keep 3 decimal, default 1),

        custom filter   inside app __init__.py
        from django.template.defaultfiles import register
        @register.filter('cus_fil')
        def cus(value):
            return value[:3]
        {{ value|cus_fil}}

    block, include, extend
        base.html   # template for reuse
        <!DOCTYPE html>
        <head><title>{% block title %} Hogwarts {% endblock %}</title></head>
        <body>
            {% block content %}{% endblock %}  # create block, can have default content inside
            {% include 'base_js.html' %}  # can't change content
        </body></html>
        index.html
        {% extends 'base.html' %}   # extend template, fill blocks
        {% block title %}{{ block.super }} Houses{% endblock %}  #  {{ block.super }}  retrieve parent block content
        {% block content %}  # block code, all {{ code }} need inside the block, no html code outside
            <ul>{% for house in houses %}
            <li>{{ house.id }} {{ house.name }}</li>
            {% endfor %}</ul>
        request path: {{ request_path }}
        {% endblock %}

        each app can have own templates folder, no need config in the settings.py
        but if referring to file with path exist in both inner app level templates and outer shared template, it will
            use the outer shared template html

        {% load static %}  # load image in template
        <p><img src="{% static 'images/hp.jpg' %}"> </p>
        <img src="/student/images/hp.jpg">
        <img src="{% static pic_src %}">

    load image
        {% load static%}
        <img src={% static '../storage/hp.jpg' %}>   path relative to STATICFILES_DIR

    error page
        404.html (must be 404)
        update settings.py  DEBUG = False

    validation
        inside model class field add validators=[method]  and define method raising ValidationError
        models.py
        class StudentValidator:
        @classmethod
        def valid_age(cls, value):
            if not re.match(r'\d{2}', str(value)):  # int must convert to string
                raise ValidationError('Incorrect age for Hogwarts')
            return True
        class Student:
            age = models.IntegerField(default=0, blank=True, null=True, validators=[StudentValidator.valid_age])


        return JsonResponse(result) (result is dict type)
        don't delete manually in database, should use manager makemigrations & migrate
        if accidentally delete table, need remove all the table after the deleted table change, and the migrations
        file under migrations folder after the deleted table change. Then makemigrations & migrate

        or use ModelForm class for validation
            common validation item: required, min_length, disabled
        admin.py  class StudentAdmin(admin.ModelAdmin):  add
            form = StudentForm

        create form.py
            from django import forms
            class StudentForm(forms.ModelForm):
                # either define validation rule for fields inside class or in Meta class
                password = forms.CharField(widget=forms.PasswordInput, label='Password', min_length=3,
                    error_messages={'required': "Password can't be empty",
                    'min_length': "Password should have more than 3 characters"})
                tag = forms.ChoiceField(choices=(('py','python'),('dj','django'))  # python in front end py in db
                class Meta:
                    model = Student
                    fields = '__all__'
                        # fields = ['name', 'password']
                    error_message = {
                        'name': {    # for 'name' field
                            'required': "Username can't be empty",
                            'max_length': 50
                            }
                        }
                def clean_password(self):   # function name: clean_ + field name
                    # execute after previous validations are passed
                    password = self.cleaned_data.get('password')
                    if all((re.search(r'\d+', password),re.search(r'[a-z]+', password),
                            re.search(r'[A-Z]+', password))):
                        return password
                    else:
                        raise ValidationError('Password need contain digit, upper case and lower case')

            form = StudentForm({'name':'Harry'})      #  StudentForm(request.POST)
            form.is_valid()     # check form data input valid
            form.cleaned_data   # return form data in a dict
            form.errors         # show the data which does not met the requirement
            form.save()         # save to database if linked model

    widgets
        form.py
        class StudentForm(forms.ModelForm):
            logo_width = forms.IntegerField(required=False, widget=ChangeImageSize, label='Logo width')
        widgets.py
        class ChangeImageSize(Input):  # parent class and inner code based on different field, check
                                       # django.forms.widgets, and related templates
            input_type = 'number'
            template_name ='change_image_size_widget.html'
        template.change_image_size_widget.html
            copy the template in django.forms.template based on different field, add more customize code inside template

    pagination
        from django.core.paginator import Paginator
        data = Student.objects.all()
        p = Paginator(data, 10)  # 10 pages
        for i in p.page_range:   # page_range generator for page number
            print([j for j in paginator.page(i)])  # paginator.page(i) return a Page object for page i
        Page object functions used for html template:
            page_num (current page number)  page(current page object) object_list (list of data in current page)
            has_next   has_previous  next_page_number   previous_page_number   len() (current page data count)

        view
        page=request.GET.get('page',1)  students = Student.objects.all()
        paginator = Paginator(students, 2) # data, size per page
        curr_page = paginator.page(page) # current page object

        html
        {% for stu in curr_page.object_list %}
            {{ stu.id }} {{ stu.name }}   {% endfor %}
        <a {% if curr_page.has_previous %} href="?page={{ curr_page.previous_page_number }}" {% endif %}>&lt;</a>
        {% for p in paginator.page_range %}
            {% if curr_page.number == p %}
                <a href="?page={{ p }}" style="color:red">{{ p }}</a>
            {% else %}<a href="?page={{ p }}">{{ p }}</a>{% endif %}{% endfor %}

    verification code
    pillow
        Image: mode(RGB, ARGB), width, height, background color (10,20,30)
        ImageDraw: bind to Image, mode(RGB, ARGB), function(text, point, line, arch)
        ImageFont: text font
        # img = Image.open('static/images/hp.jpg')  # draw on image
        img = Image.new('RGB',(80,40), (100,100,0)) # mode(RGB,ARGB), (width,height), bg (rgb)color. draw on white sheet
        draw = ImageDraw.Draw(img, 'RGB')  # image object, mode
        font_color = (0, 20, 100)
        font = ImageFont.truetype(font=os.path.join('static', 'fonts', 'Pacifico.ttf'), size=20)
        draw.text((5,5), 'Hello', font=font, fill=font_color)  # start (x,y) coordinates, draw text
        draw.line((0, 0) + img.size, fill=font_color)   # img.size is [80,40]  same as (0,0,80,40)
        draw.point((10, 30), (255,0,0))  # (x,y) (r,g,b)
        buffer = BytesIO()
        img.save(buffer, 'png')  # write img
        del draw  # delete draw
        return HttpResponse(content=buffer.getvalue(), content_type='image/png')

    csrf
        settings file default django.middleware.csrf.CsrfViewMiddleware is added in the MIDDLEWARE
        generate hidden input  name='csrfmiddlewaretoken' value is generated during render template, and save it
        in session, when form is post to server, use CsrfViewMiddleware do validation
        html template:
        <form method="post">
            {% csrf_token %}  # put inside form
        </form>
        or remove django.middleware.csrf.CsrfViewMiddleware in settings.py
        or add @csrf_exempt on view function
            @csrf_exempt
            def add_student(request):
        or in urls.py
            path('add', csrf_exempt(add_student)),
        django.contrib.auth.hasher.make_password(password)  # cipher the password
        password = make_password(password)
        if check_password(password, user.password)   # password from post request not encrypted, user.password encrypted

    mysql
        settings.py
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'company',
                'USER': 'cai',
                'PASSWORD': '123456',
                'HOST': '127.0.0.1',
                'PORT': '3306',
                'CHARSET': 'utf8'
            }
            'db1': {    # distributed database (split data inside multiple db)
                        # 1. base on id // record per server, can't use default auto increase id. fast find db,
                            easy extend db. but each new db has higher load sometime, uneven load distribution,
                            fix cost for low load db
                          2. base on id % # server (rotation distribute id to db). even load distribution across
                            database, but more initial cost(can put multiple db on single server initially), hard to
                            extend more database
                        # id = cache.incr(id)  # generate id in cache
                            # other distributed ID generator: MongoDB object_id,  MAC address  commit_id, UUID
                                # machine id, process id, thread id, time stamp, serial number
                        # use Students.objects.using('db1').get(id=1)
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'company',
            }
        }
        __init__.py
        import pymsql
        pymsql.install_as_MySQLdb()   # alternative of install mysqlclient  or use navicat



    request (extend wsgi request)
        request object generated by django framework
        request include headers (method, content_type, path, path_info, get_full_path), request path, url, cookie
        (request.COOKIES), file, body byte content, query param (request.GET), form param (request.POST), session
        request.GET (query param after ?) / POST (only post request form param) / COOKIES (all client cookies info) /
            FILES (all files inside form, MultiValueDict class object, inside is InMemoryUploadedFile) / sessions (data
            stored in session, accessible via multiple request) / META (wsgi
            request meta info(client request info, server environment),REMOTE_ADDR (ip address), PATH_INFO, REQUEST_
            METHOD, QUERY_STRING, CONTENT_TYPE) are QueryDict object, can encode url with utf-8 character
        request.method (GET, POST, PUT, DELETE) / path (not including param, ip port) / request.get_raw_uri (unique
            resource identifier, used for restful, same as url (locator), contain ip, port, path, param) /content_type
            (text/html) / encoding / body (byte stream data, ex.json data in post request, add PUT update data in body)
        request.user   return current login user, if no one is login, default is AnonymousUser
        request.META.get('REMOTE_ADDR')  # can access other header information with different key
        request.META['HTTP_USER_AGENT']
    response
        response object is returned by the view functions, can use django render() / redirect() to generate response
        or use HttpResponse (extend HttpResponseBase), HttpResponseRedirect, JsonResponse
        attributes inside response: content (for HttpResponse: byte or string, for JsonResponse: dict), status code,
            content_type
        return HttpResponse(content=img, content_type='image/jpeg')
        return HttpResponse(content='Hi', status=200, content_type='text/html;charset=utf-8')  # string
        return HttpResponse('<h1>hi, Django</h1>'.encode('utf-8'))   # byte
        return HttpResponse(content=json.dumps({'msg': 'hi'}),content_type='application/json')  # json
        return JsonResponse({'msg': 'hi'})  # json

    cookie
        HttpResponse.set_cookie()  # key, value, max-age(default none: 2 weeks, 0: till browser close, not specify:
            forever, 100: 100 sec) expires (datetime), don't support chinese, can't use different browser,
            cors( domain, protocol, port)
        HttpRequest.COOKIES.get('username')  # get cookie value via key
        HttpRequest.delete_cookie('username')   # delete cookie
        resp = HttpResponse(content=img)   # resp = render(request, 'detail.html', locals())
        resp.set_cookie('token', token, expires=datetime.now()+timedelta(minutes=2))
        resp.delete_cookie('token')  # delete cookie
        request.COOKIES # get all cookies

    session
        django save session inside django_session table in database (key, value, expiration_date (default 2 weeks))
        session is depend on cookie. if client browser disable cookie, session will not work.

        request.session[key]=value  # HttpRequest.session[key]=value
        request.session.get(key)
        del request.session["key"]
        request.session.set_expiry(100)  # 100 seconds

        request.session.clear()  # delete all session
        view1
        request.session['student'] = json.dumps({'user': student.name, 'id': student.id})
        view2
        info = request.session.get('student')  # {"user": "Harry Potter", "id": 1}


    view
        django view has 2 implementation:
            function-based view (FBV): define view base on function (same function handle different method(get, post)
                become messy)
            class-based view (CBV): based on OOP, extension, override property. extend view, use dispatch internally

        class-based view CBV:
            from django.views import View
            many classes: View, TemplateView, RedirectView, ListView, EditView, FormView, DetailView, DeleteView
            pass in url parameter inside function *args **kwargs
                urls: path('login/<name>',LoginView.as_view())
                views.LoginView.  def get(self, request, id):  name = id = kwargs.get('name')
        urls.py
            path('login',LoginView.as_view())
            path('srudent/<id>/',StudentView.as_view())
            path('query/<id>/',QueryView.as_view(), name='query' )   # redirect view must have parameter
        views.py
            class LoginView(View):
                def get(self, request):  # def get(self, request, id):  *args, **kwargs if have request parameter
                    id = kwargs.get('id')
                    return render(request, 'login.html', locals())
                def post(self,request):
                     return HttpResponse('Put Request')

            class StudentView(TemplateView):  # load template, only for get method
                template_name = 'list.html'
                extra_content = {'msg': 'additional info'}  # html {{ msg }}  {{ id }}

                def get_context_data(self, **kwargs):  # override get context data (optional)
                    context = super(StudentView, self).get_context_data(**kwargs)
                    id = context.get('id', 0)
                    context['data'] = ['a'] if id !=0 else ['b']  #  html {{ for i in data }}
                    return context
                # dispatch() http_method_not_allowed()

            class QueryView(RedirectView):  # load template, only for get method
                url  #redirect url or pattern
                pattern_name = 'hogwarts:query'
                query_string = True  # confirm whether have request param in the url
                def get_redirect_url(self, *args, **kwargs):  # override parent (optional)
                    student = get_object_or_404(Student, pk=kwargs['pk'])
                    student.update_counter()
                    return super(QueryView, self).get_redirect_url(*args,**kwargs)
                # dispatch() http_method_not_allowed()
    middleware
         aop(add functionality before and after function/request, and will not affect original code)
            add additional code dynamically, similar to decorator. Used for session, csrf, authorization, ip black/white
            list, limit request frequency, logging, statistic, logging exception
        5 hook functions
        browser ->(process_request)-> url dispatcher ->(process_view)-> views -> models -> views -> (process_template_
            response)-> templates -> (process_response) -> browser  (process_exception: monitor exception whole process)
        middleware is for all requests, responses
        process_request(request): between django framework to url dispatcher
        process_view(request, callback, callback_args, callback_kwargs): between url dispatcher to view functions
        process_template_response(): between view function and template rendering (not frequent use)
        process_response(request, response): between return HttpResponse to client browser receive
        process_exception(request, exception): monitor exception during whole process from request to response

        settings.py
        MIDDLEWARE add 'middleware.check_login.CheckLoginMiddleWare'

        add middleware folder check_login.py
        from django.utils.deprecation import MiddlewareMixin
        class CheckLoginMiddleWare(MiddlewareMixin):
        def process_request(self, request):
            print('---CheckLoginMiddleWare---', 'process request')
            msg = '%s visited %s' %(request.META.get('REMOTE_ADDR'), request.get_raw_uri())
            logging.getLogger('django').info(msg)
            #print(request.path, request.COOKIES)
            if request.path not in ('/student/login', '/') and not request.path.startswith('/admin/'):
                if not request.session.get('student') or not request.COOKIES.get('token'):
                    return redirect('/student/login')

        def process_view(self, request, callback, callback_args, callback_kwargs):
            # callback is calling view function
            print('---CheckLoginMiddleWare---', 'process view')
            # callback_kwargs['page']=request.GET.get('page',1)   # view: page = kwargs.get('page',5 )
                        # modify parameter when url is not allowing add parameter, view function must have page
            print(callback, callback_args,callback_kwargs)

        def process_response(self, request, response):
            print('---CheckLoginMiddleWare---', 'process response')
            return response    # must return


        def process_exception(self, request, exception):
            #print('---CheckLoginMiddleWare---', 'process exception')
            print(exception)
            if isinstance(exception, StudentError):
                return HttpResponse('Something went wrong: %s' % exception)

        class StudentError(Exception): # declare specific exception easier for trace source
            pass
        raise StudentError('wrong student')  # raise exception in code


    logging
        component of logger: version, formatters, handlers, loggers (default django, or django.request), filters

        settings.py
        LOGGING_DIR = os.path.join(BASE_DIR, 'log')   # create a log directory

        LOGGING = {
            'version': 1,   # must have logger version
             'disable_existing_loggers': False,   # disable existing logger
             'formatters': {   # declare logger formatter
                 'simple': {   # declare new formatter named simple
                     'format': '[%(asctime)s] %(module)s.%(funcName)s %(levelname)s : %(message)s',
                     'datefmt': '%Y-%m-%d %H:%M:%S'
                 }
             },
            # handlers：
             'handlers': {  # declare logging handler for different need (io, console output, email, default...)
                 'mail_admins':{
                     'level': 'ERROR',
                     'class': 'django.utils.log.AdminEmailHandler',
                     'include_html': True,
                 },
                 'default': {
                    'level': 'DEBUG',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': os.path.join(LOGGING_DIR, 'run.log'),
                    'maxBytes': 1024*1024*5,
                    'backupCount': 5,
                    'formatter': 'simple',
                    #'when': 'W0'  #every monday cut logger
                 },
                 # 'request_handler': {
                 #     'level': 'DEBUG',
                 #     'class': 'logging.handlers.RotatingFileHandler',
                 #     'filename': os.path.join(LOGGING_DIR, 'debug_request.log'),
                 #     'maxBytes': 1024*1024*5,
                 #     'backupCount': 5,
                 #     'formatter': 'standard',
                 # },
                 'file_handler': {
                    'class': 'logging.FileHandler',
                    'level': 'WARNING',
                    'formatter': 'simple',
                    'filename':os.path.join(LOGGING_DIR,'file_io.log'),
                 },
                 'console': {
                     'level': 'INFO',
                     'class': 'logging.StreamHandler',  # use 'logging.StreamHandler' to output to console
                     'formatter': 'simple',
                 },
             },
             'loggers': {   # declare logger
                 'django': {
                     'handlers': ['console', 'default'],
                     'level': 'INFO',
                     'propagate': True,  # whether parsing to other logger  have a child django.request
                 },
             },
        }
        # using logger inside view or middleware...
        logging.getLogger('name').info(msg)  # name is logger name  error()  warn()  critical()


    cache
        settings.py
        CACHES = {
            'file_cache': {        # save cache in file
                'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',   # must have
                'LOCATION': os.path.join(BASE_DIR, 'cache'),   # must have
                'TIMEOUT': '300',  #second
                'KEY-PREFIX':'cc',
                'VERSION':'1',
                'OPTIONS': {
                    'MAX_ENTRIES': '300',
                    'CULL_FREQUENCY': 3    # remove 3% cache if full
                }
            },
            'html_cache': {        # save cache in memory
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': 'unique-snowflake'
            },
            'default':{  #redis cache
                'BACKEND': 'django_redis.cache.RedisCache',
                'LOCATION': 'redis://127.0.0.1:6379/1',
                'OPTIONS':{
                    'CLIENT_CLASS': 'django_redis.client'
                }
            }

        }

        use native cache methods
        from django.core.cache import cache
        cache.add(key, value, timeout=60)  # add cache set timeout seconds,  version optional
        cache.set(key, value, timeout=60)  # add cache set timeout seconds
        cache.has_keys(key)  # find all cache key
        cache.get(key)
        cache.delete(key)
        cache.set_many()    cache.get_many()   cache.clear()  cache.delete_pattern('cc_student*')
        caches['html_cache'].has_key(request.path)   # non default cache
        refer to middleware.html_cache.CachePageMiddleware

        cache webpage, save render time, cache for x seconds, return cache instead of render again
        @cache_page  # add in front of view function, request blocked during cached period
        or cache.set()/add(html)  at middleware:  process request() check cache and return if exist,
            process_response() add cache

        @cache_page(timeout=5, cache='html_cache',key_prefix='site1')  # cache name and prefix  timeout count refresh
            # page, cache default use 'default' cache

        redis cache
        pip install django-redis
        function: add,   get,   delete,   clear,  delete_many,   get_many,    set_many,  incr,  decr,  has_keys
            keys,   iter_keys,   ttl,   presist,   lock,  close,   touch (keep data not delete when cache full)

        cache.add('student', json.dumps({'user': student.name, 'id': student.id}), timeout=100)
        cache.get('student')  # {"user": "Harry Potter", "id": 1}
            # redis key is :1:student  for use db 1

        # store session in redis, need config redis CACHE first
        SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
        #SESSION_COOKIE_NAME = 'SESSION_ID'
        #SESSION_COOKIE_PATH = '/'
        SESSION_CACHE_ALIAS = 'default'   # change to redis cache (default is set to redis in CACHES)
        SESSION_COOKIE_AGE = 1209600   # in seconds


        # rewrite orm operation
        db.py
            def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
                self._origin_save(force_insert, force_update, using, update_fields)
                key = 'Model-%s-%s' % (self.__class__.__name__, self.pk)
                cache.set(key, self)

            def patch_model():   # monkey patch
                models.Model._origin_save = models.Model.save
                models.Model.save = save

        from db import patch_model
        patch_model()  # then save method will add to cache

    signals
        django.db.models.signals: pre_init, pre_save, pre_delete, m2m_changed, class_prepared, pre_migrate (post)
        django.core.signals: request_started, request_finished, get_request_exception, setting_changed,
        django.test.signals: template_rendered
        django.db.backends.signals: connection_created

        inside __init__.py  (import model class inside function to avoid cycling reference)
        def model_delete_pre(sender, **kwargs):  # sender is mainapp.models.Student (model.Model child class)
                                                 # kwargs: signal:sender(django.db.models.signals.ModelSignal)
                                                 # using: db name (default)  instance:Student object(1)
            print(issubclass(sender, Student))  # true
            print(isinstance(sender, Student))  # false
            print(sender is Student)  # true
            print(sender == Student)  # true
            print(sender, kwargs)
        pre_delete.connect(model_delete_pre)  # bind signal to function


        # or use decorator
        @receiver(pre_save)
        def uuid_pre_save(sender, **kwargs):
            if issubclass(sender, Student):
                instance = kwargs.get('instance')
                if not instance.id:
                    instance.id = uuid.uuid4().hex

    # self defined signal, define, post and receive signal.  use to split work among teams (send data across app)
    inside mainapp.__init__.py   # define
        from django import dispatch
        codeSignal = dispatch.Signal(providing_args=['path','name'])  # declare keys param list sending inside signal

    inside method   # send
        mainapp.codeSignal.send('api',path=request.path, name=student.name)
            #sender name, keys values in side param list to send

    inside djangoSample.__init__.py  # receive
        @dispatch.receiver(codeSignal)
        def receive_signal(sender, **kwargs):
            print(sender, kwargs)   # sender: <django.dispatch.dispatcher.Signal>  kwargs: path='/xxx', name='xxx'


    high volume asynchronous handling
        use Celery + Redis() / RabbitMQ  to solve C10K problem (broker+ workers handle high concurrency)
        Celery is an asynchronous task queue/job queue based on distributed message passing. It is focused on real-time
        operation, but supports scheduling as well
        Celery only provide interface not implementer, set broker implementing method (redis publish/subscribe,
        RabbitMQ, MongoDB,)

        Celery class assignment and control execution
        broker(queue) send task message to many workers, and collect execution result
        worker (backend process) handle task execution

    pip install celery eventlet          django-redis flower (gui optional)
    pip install django-celery-results
    settings.py     # check celery document for new version keywords
        INSTALLED_APP  add 'celery','django_celery_results',  # 'djcelery'
        BROKER_URL = 'redis://127.0.0.1:6379/2'
        CELERY_TIME_ZONE = 'America/Chicago'
        CELERY_RESULT_BACKEND = 'django-db' # using django_celery_results, can use redis as well
        CELERY_CACHE_BACKEND = 'default'  # optional
        CELERY_TASK_SERIALIZER = 'json'  # task serialize and deserialize,  'pickle' less limitation, better performance
            # json serializer will convert int key to string
        CELERY_RESULT_SERIALIZER = 'json'
        # broker_pool_limit = 100 # default 10
        # result_cache_max = 10000  # max result cache count
        # result_expires = 3600  # result expire  in second
        # CELERY_IMPORTS = ('mainapp.tasks',)   # manual import task not needed if app.autodiscover_tasks()
        # from celery.schedules import timedelta, crontab   # for schedule tasks

    main project add celery.py
        from __future__ import absolute_import # absolute path import
        from celery import Celery
        import os
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoSample.settings")   # use project name
        app = Celery('hogwartsCelery', broker='redis://127.0.0.1:6379/2')  # backend='redis:127.0.0.1:6279/2'
            # app = Celery('hogwartsCelery') add broker config in settings
        app.config_from_object("django.conf:settings") # specify the settings file name for celery settings.py
        # app.conf.timezone = "Asia/Shanghai"
        app.autodiscover_tasks()  # auto discover task


    main project  __init__.py
        from __future__ import absolute_import
        from .celery import app as celery_app
        __all__ = ('celery_app',)   # add celery_app object inside project

    mainapp  add tasks.py  # default name is tasks.py
        from celery import shared_task
        import time
        @shared_task
        def hello_celery(name):
            print('hello Hogwarts')
            time.sleep(2)
            print(name)
        @app.task
        def add(a, b):
            time.sleep(2)
            return a+b
        add.delay(2,3) to call task

        @after_task_publish.connect(sender = 'mainapp.tasks.hello_celery')
        def task_sent_handler(sender=None, headers=None, body=None, **kwargs):
            print(sender)

            @before_task_publish,  @after_task_publish, @task_prerun, @task_postrun, @task_success,
            @task_failure, @task_revoked

        def async_celery(func):  # define decorator similar to @app.task, but no need delay
            task = app.task(func)
            return task.delay

        @async_celery
        def add(x, y):
            return x+y

        add(2,3)  # will call the delay function automatically with @async_celery, instead of add.delay(2,3)

    start celery
        python manage.py migrate django_celery_results    # generate result table
        celery -A djangoSample worker -P gevent  -l info      # -P Coroutines (for windows)    -l log
            # eventlet not working   use solo / gevent    -A task   create worker
        hello_celery.delay('Harry')  # call async task
        add.delay(2,3)  # call async task
    res = hello_celery.delay(1, 2)  # calling tasks
    res.ready()  # check task done or not
    res.result  # print result

    schedule
    pip install django-celery-beat
    settings.py
        CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'
        from celery.schedules import crontab
        CELERYBEAT_SCHEDULE = {
            "schedule_my_task": {
                "task": "mainapp.tasks.hello_celery",
                "schedule": crontab(minute="01", hour="15"),  # default number, in second
                "args": (2,3)
            }
        }


    REST
    representational state transfer, based on action return result page
    rules for RESTful API:
        1. each resource set URI (unique resource identifier)
        2. transfer data via JSON/XML
        3. no state connection (server don't save context, each request is independent)
            (use token instead of session saving authorization info)
        4. HTTP action: GET, POST, PUT, DELETE
        5. avoid using verb, version number, query string   GET /user/book?id=3
    for two table relation, using serializers.ModelSerializer (get object in json) or HyperlinkedModelSerializer
        (get url for object in json, need view for both class)
    or write custom serializer, need declare model fields(parameter), implement create(**validate_data) and
        update(**validate_data) functions.
    serializer internally use rest_framework JSONRenderer and JSONParser (deserialize)


    pip install djangorestframework
    pip install markdown       # markdown (text-to-HTML conversion) support for the browsable api
    pip install django-filter  # filtering support

    settings.py
        INSTALLED_APPS  add  'rest_framework',

        REST_FRAMEWORK = {
            # Use Django's standard `django.contrib.auth` permissions,
            # or allow read-only access for unauthenticated users.
            'DEFAULT_PERMISSION_CLASSES': [
                'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
            ]
        }
    api __init__
        from rest_framework import routers
        from mainapp.api.students_api import StudentAPIView
        api_router = routers.DefaultRouter()
        api_router.register('students', StudentAPIView)  #ViewSet
        #api_router.register('houses', StudentAPIView)  # if use HyperlinkedModelSerializer

    or urls.py
        urlpatterns = [
            path('admin/', admin.site.urls),
            path('api/', include('mainapp.urls')),
        ]

    APIView: HTTP method: GET, POST, PUT, PATCH, DELETE
    ViewSet: CRUD operation: LIST, CREATE, RETRIEVE, UPDATE, DESTROY, usually use router generate url

    mainapp.urls.py
        urlpatterns = [
            path('student/', StudentAPIView.as_view(), name='student'),   # APIView, no need specify mapping
            path('student/<int:pk>/', StudentAPIView.as_view(), name='student-detail'),
            url('student/', StudentAPIView.as_view({   # ViewSet (not recommended), use router instead
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            }),name="student_detail"),
        ]
    mainapp.api.student_api
        from rest_framework import serializers, viewsets
        from mainapp.models import Student, House
        class HouseModelSerializer(serializers.ModelSerializer):
        # serializers.ModelSerializer  have create and update method, implement data validator
        # "house": 1
            class Meta:
                model = House
                fields = ('id', 'name')

        class StudentModelSerializer(serializers.ModelSerializer):
            # house = HouseModelSerializer()   # (many=True) if one side  nested serializer
            class Meta:
                model = Student
                fields = ('id', 'name', 'age', 'house','password')
            # StudentModelSerializer(student).data return {'name': 'harry', 'age': 11, 'house': <House object 1>}

            # def create(self, validated_data):   # don't support house.name, otherwise no need
            #     if no house serializer will not be serialized and linked
            #     print(validated_data)  #{'name': 'harry', 'age': 11, 'house': {'name': 'Gryffindor'}}
            #     student = Student.objects.create(**validated_data)
            #     return student

        class StudentAPIView(viewsets.ModelViewSet):   #
            queryset = Student.objects.all()
            serializer_class = StudentModelSerializer

    or use serializers.HyperlinkedModelSerializer  need view for both class if relationship
            "house": "http://localhost:8000/api/houses/1/",
        class HouseModelSerializer(serializers.HyperlinkedModelSerializer):
            age = serializers.IntegerField(required=False, default=10)  # add field need serialize
            # Relation serializing ways:
            #students = serializers.StringRelatedField(many=True)  # change from hyperlink/id to string object
            #students = serializers.PrimaryKeyRelatedField(many=True)  # change from hyperlink to id
            # serializers.HyperlinkedRelatedField default for HyperlinkedModelSerializer
            students = serializers.SlugRelatedField(many=True,queryset=Student.objects.all(), slug_field='name')
                # must add read_only=True or provide `queryset` argument
            students = serializers.ManyRelatedField(serializers.SlugRelatedField(slug_field="username", source="user_id"),
                                             queryset=User.objects.all(), source="follow")
            # change from hyperlink to interested field (slug_field),
            class Meta:
                model = Student
                fields = ('id', 'name', 'age', 'house','password')
        class HouseAPIView(viewsets.ModelViewSet):
            queryset = House.objects.all()
            serializer_class = HouseModelSerializer


    Serialize and deserialize
        StudentModelSerializer input parameter: data, instance, context, partial, many

        dic_org = StudentModelSerializer(student).data   # return OrderedDict,  param student object
        content = JSONRenderer().render(dic_org)  # return bytestring  # dict => string
        buffer = BytesIO(content) # byte stream
        dic = JSONParser().parse(buffer)  # return Dict

        parse post request data, save object
            data = JSONParser().parse(request)  # byte => dict
            serializer = StudentModelSerializer(data=data)
            serializer.save  # save object with OrderedDict serializer
            serializer.is_valid()
            serializer.data

    Restframework request, response
        request.POST  # only get form data in 'POST' method
        request.data  # in rest_framework extend HttpRequest, get arbitrary data,  works for 'POST' 'PUT' 'PATCH'

        return Response(data)  # extend TemplateResponse, need provide data

        rest_framework.status  provide all status code (ex. HTTP_400_BAD_REQUEST)

        @api_view(['GET','POST'])
        @permission_classes((permissions.AllowAny,))   # solve  does not set `.queryset` error
        def student_list_api(request):
            data = Student.objects.all()
            serializer = StudentModelSerializer(data, many=True)
            return Response(serializer.data)

        or use class based view
        class StudentAPIView(APIView):
            @permission_classes((permissions.AllowAny,))
            def get(self, request, **kwargs):
                id = kwargs['id']
                student = Student.objects.get(pk=id)
                serializer = StudentModelSerializer(student)  # instance=self.student
                if serializer.is_valid():
                    serializer.save()
                return Response(serializer.data)

            @permission_classes((permissions.AllowAny,))
            def put(self, request, **kwargs):
                id = kwargs['id']
                student = Student.objects.get(pk=id)
                serializer = StudentModelSerializer(student, request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data,status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    Rest api authentication
        default no need for authentication for using api
        settings.py    REST_FRAMEWORK add
            'DEFAULT_AUTHENTICATION_CLASSES': [
                'rest_framework.authentication.BasicAuthentication',
                # only for https, and need request authentication after login, not save authentication in session
                # based on username pwd
                'rest_framework.authentication.SessionAuthentication',  # based on session
                #'rest_framework.authentication.TokenAuthentication'  # based on token (inside header)
            ]
            INSTALLED_APPS   add  'rest_framework.authtoken',
        terminal: python manage.py migrate
            python manage.py drf_create_token cai  # b1694f8ec22c3a5749b221cf8993cf8cc83c9880
            curl -X GET http://127.0.0.1:8000/student/student_api/1 -H "Authorization: Token
                b1694f8ec22c3a5749b221cf8993cf8cc83c9880"
            or use ajax in html with header
                <button onclick="ajax_get()">get data</button>
                <p id="data"></p>
                function ajax_get(){
                    fetch('/student/student_api/1',{
                        headers:{
                            'Authorization': 'Token b1694f8ec22c3a5749b221cf8993cf8cc83c9880'
                        }
                    }).then(resp=>resp.json())
                        .then(data=>{
                            data =JSON.stringify(data)
                            document.getElementById('data').innerHTML= data
                        })
                }


        or instead of settings.py
        add in view.py  inside class View
        class StudentAPIView(APIView):   # authentication_classes only can be add in CBV, not FBV
            authentication_classes = (TokenAuthentication,)  #SessionAuthentication, BasicAuthentication
            # this will also include authentication in settings.py
            permission_classes = (IsAuthenticated,)

        or instead of generate token via manage.py, write inside views.py
        from django.contrib.auth.models import AnonymousUser, User
        from rest_framework.authtoken.models import Token
        class StudentAPIView(APIView):
            def get(self, request, id):
                user = User.objects.filter(username=request.user)   # django model user
                if request.user is not AnonymousUser:
                    token = Token.objects.get_or_create(user=user.first())
                    request.session['token'] = token


        Create own Authentication
            create class MyAuthentication(BaseAuthentication):
                rewrite def authenticate(self, request):
                            token = request.query_params.get('token') ...
            add MyAuthentication inside authentication_classes in class view or global settings.py
            add generate token logic inside view function

    run curl to get json response
    curl -X POST -H "Content-Type: application/json" http://127.0.0.1:8000/api/Student/ -d "{\"student_name\":\"Harry\"}"

    django send email
        settings.py
            EMAIL_HOST = 'smtp.gmail.com'
            EMAIL_PORT = 587    # gmail tls port
            EMAIL_HOST_USER = 'caichenghao11@gmail.com'
            EMAIL_HOST_PASSWORD = 'xwxrtmmtejqeodod'   # not email login password
                    # check https://kinsta.com/blog/gmail-smtp-server/
            EMAIL_USE_TLS = True

        views.py
        from django.core.mail import send_mail
        def send_student_email(request,email)
            title, msg = 'Student forget and change password', ''
            html ='<html> Dear student, please change your password <a href="https://www.baidu.com">here</a>'
            send_mail(title, msg, from_email='caichenghao11@gmail.com', html_message=html, recipient_list=[email])


    CORS   via django-cors-header   # solve json csrf problem
        pip install django-cors-headers
        settings.py   MIDDLEWARE add
            'corsheaders.middleware.CorsMiddleware',   # must before CommonMiddleware, better put at first

            COS_ALLOW_CREDENTIALS = True  # declare backend accept cookie
            COS_ORIGIN_ALLOW_ALL = True   # allow all ip visit
            COS_ORIGIN_WHITELIST =('*')   # white list allow   ("ip1:port","ip2:port")
            ALLOWED_HOSTS = ['*']   # white list  ["ip1","ip2"]
            # CORS_ALLOW_METHODS = ('DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT') # optional allowed method
            # CORS_ALLOW_HEADERS = ('XMLHttpRequest', 'X_FILENAME', 'accept-encoding', 'authorization', 'content-type',
               # 'dnt', 'origin', 'user-agent', 'x-csrftoken', 'x-requested-with', 'Pragma',)  # optional allowed header


    django scripts
        #!/usr/bin/env python
        import django
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # __file__:  current file
        sys.path.insert(0, BASE_DIR)   # add BASE_DIR to the system path first in the list
        os.environ.setdefault("DJANGO_SETTINGS_MODULE","djangoSample.settings")  # add django setting filr
        django.setup()


    static resources
        program required resources can save on nginx servers cluster (has cache)
        user upload data save on cloud storage (aws s3), using content delivery network technology

    stress testing
        tool: apache benchmark, siege, webbench, wrk
        indicator: RPS(max request per second can withhold), QPS(query per sec), TPS(transaction per sec)
            apt-get install apache2-utils
            ab -n 1000 -c 300 httpL//127.0.0.1:9000/   # number of request, concurrency, -t timelimit
                # this will generate a stress test report

        TCP has blocked state waiting for receive data. this will cause problem for large RPS
            Use multi process (manage by os), threading, coroutines

    context: state stored and read during cpu switching tasks every several milliseconds
    process: ~MB, communication: socket, pipe, file, shared memory, UDS. context switching a bit slower, not flexible, controlled by
        operating system. but more stable
    thread: ~kb, communication: direct transfer information. context switching a bit faster, not flexible, controlled by
        python interpreter. wasting cpu resource if process / thread blocking
    Coroutines: <1k, communication: same as thread.  context switching fast and flexible (controlled by programmer)
    high performance context switching: blocked task take no cpu time, only switch to the blocking task after receive
        an I/O event notification (listened by OS interface: select, poll, epoll(add event in readied queue instead of
        looping listening to event))
    event driven: take action after receiving an event. Nginx (40000+ RPS), (110000+ Redis), (5000+ Tornado)
    compare to Django 500 RPS

    multi-process(used because of global interpreter lock, limit to 1 task per process at any time send to cpu)
        + mult-coroutine implementation for performance, allowing multiprocessors handling multiple tasks for
        multi-process

    use Gunicorn as HTTP server to run django for multi-process+ mult-coroutine
        User request send to Gunicorn server, then using multi-coroutine task lib  using wsgi (web server gateway
            interface) communication interface to process django app
            HTTP server: start or stop client connection, send/receive client data
            WSGI: convert client request message to HTTPRequest object, convert app HttpResponse to response message

        # RPS 5000 RPS  if has database operation:300 RPS single db
        gunicon-config.py        # check official site for more config info
            from multiprocessing import cpu_count


        start gunicorn
            gunicorn -c djangoSample/gunicon-config.py djangoSample.wsgi

        watch -n 0.5 "ps ax|grep -v grep|grep gunicorn|awk '{print $1}'"
        ps ax|grep -v grep|grep gunicorn


        file descriptor: ulimit -n 65535    # change max file open in terminal   # 10240 for mac
        core limitationL net.core.somaxconn
        memory limitation

        Nginx: reverse proxy at front of gunicorn, and also for load balancing (default roll polling, weight, ip_hash,
            least_connn)
            download Nginx (official site/ aptget)
            run: ./configure in terminal
            run: make   # compile file inside objs
            make install    # install at /usr/local/nginx
            change config at /usr/local/nginx/conf/nginx.conf
                user root;  # can't kill by other non root superuser
                worker_processes  4;
                pid /run/nginx.pid   # save pid in file
                events{
                    worker_connections 10240;
                }
                http {
                    include     mime.types
                    default_type  application/octet-stream;
                    log_format main '$time_local $remote_addr $status $request_time '
                                    '$request [$body_bytes_sent/$bytes_sent]    '
                                    '"$http_user_agent" "$http_referer"';
                    sendfile            on;
                    tcp_nopush          on;
                    keep_alive_timeout  65;
                    gzip                on;
                    upstream app_server{
                        server 127.0.0.1:9000 weight=10;   # send to gunicorn
                        # add more server here will enable load balance
                    }

                }
                server{
                    listen          80;
                    server_name     djangoSample.caichenghao.org;
                    access_log      /opt/djangoSample/logs/access.log  main;
                    error_log       /opt/djangoSample/logs/error.log;

                    location = /favicon.ico {
                        empty_gif;
                        access_log off;
                    }
                    location /static/ {
                        root  /opt/djangoSample/frontend/;
                        expires 30d;
                        access_log off;
                    }
                    location / {
                        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                        proxy_set_header Host $http_host;
                        proxy_redirect off;
                        proxy_pass http://app_server;
                    }
                }

            nginx -c conf/nginx.conf   # start nginx proxy

        ssh root@xxx.xxx.xxx.xxx    # windows xshell
        ssh-keygen    # public key ~/.ssh/id_rsa.pub    # private key: ~/.ssh/id_rsa
            copy public key to server  ~/.ssh/authorized_keys
        put code in /opt  or  /project
        rsync -crvP --exclude={.git,.venv,logs,__pycache__} ./ root@xxx.xxx.xx:/opt/djangoSample/
            check server cpu:  cat /proc/cpuinfo    check server  memory:  free -m


    scripts
        celery-start.sh
            #!/bin/bash
            celery worker -A worker --loglevel=info

        setup.sh
            #!/bin/bash
            system_update() {
                echo 'Start updating system...'
                apt update -y
                apt upgrade -y
                echo -e 'System update finished.\n'
            }
            install_software() {
                echo 'Start installing system component...'
                BASIC='man gcc make sudo lsof ssh openssl tree vim language-pack-zh-hans'
                EXT='dnsutils iputils-ping net-tools psmisc sysstat'
                NETWORK='curl telnet traceroute wget'
                LIBS='libbz2-dev libpcre3 libpcre3-dec libreadline-dev libsqlite3-dev libssl-dev zlib1g-dev'
                SOFTWARE='git mysql-server zip p7zip apache2-utils sendmail'
                apt install -y $BASIC $EXT $NETWORK $LIBS $SOFTWARE

                echo 'Cleaning temp files'
                apt autoremove
                apt autoclean

                echo 'setting chinese environment'
                locale-gen zh_CN.UTF-8
                export LC_ALL='zh_CN.utf8'
                echo "export LC_ALL='zh_CN.utf8'" >> /etc/bash.bashrc

                echo 'start mailing service'
                service sendmail start

                echo -e 'System component installed'
            }
            install_nginx() {
                echo 'Start installing Nginx...'
                if ! which nginx > /dev/null     # if able to export then already installed
                then
                    wget -P /tmp 'http://nginx.org/download/nginx-1.14.1.tar.gz'
                    tar -xzf /tmp/nginx-1.14.1.tar.gz -C /tmp
                    cd /tmp/nginx-1.14.1
                    ./configure
                    make
                    make install
                    cd -
                    rm -rf /tmp/nginx*
                    ln -s /usr/local/nginx/sbin/nginx /usr/local/bin/nginx
                    echo -e 'Nginx installed.\n'
                else
                    echo -e 'Nginx already exist.\n'
                fi
            }
            install_redis() {
                echo 'Start installing Redis...'
                if ! which redis-server > /dev/null     # if able to export then already installed
                then
                    wget -P /tmp 'http://download.redis.io/releases/redis-5.0.0.tar.gz'
                    tar -xzf /tmp/redis-5.0.0.tar.gz -C /tmp
                    cd /tmp/redis-5.0.0
                    make && make install
                    cd -
                    rm -rf /tmp/redis*
                    ln -s /usr/local/nginx/sbin/nginx /usr/local/bin/nginx
                    echo -e 'Redis installed.\n'
                else
                    echo -e 'Redis already exist.\n'
                fi
            }
            install_pyenv() {
                echo 'Start installing pyenv...'
                if ! which pyenv > /dev/null     # if able to export then already installed
                then
                    curl -L /tmp 'https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash'
                    export PATH="$HOME/.pyenv/bin:$PATH"
                    eval "$(pyenv init -)"
                    eval "$(pyenv virtualenv-init -)"
                    echo -e 'pyenv installed.\n'
                else
                    echo -e 'pyenv already exist.\n'
                fi
                pyenv update
            }
            set_pyenv_conf() {
                echo -e 'starting config pyenv'
                cat >> $HOME/.bashrc << EOF
                # PyenvConfig
                export PATH="$HOME/.pyenv/bin:$PATH"
                eval "\$(pyenv init -)"
                eval "\$(pyenv virtualenv-init -)"
                EOF
                source $HOME/.bashrc
                echo -e 'pyenv config finished.\n'
            }
            install_python() {
                echo -e 'starting install python 3.6'
                if ! pyenv version|grep 3.6.7 > /dev/null;
                then
                    pyenv install -v 3.6.7
                    echo -e 'python 3.6 installed.\n'
                else
                    echo -e 'python 3.6 already exist.\n'
                fi
                pyenv global 3.6.7
            }
            project_init(){
                echo 'Setting up project environment'
                proj='/opt/djangoSample/'
                mkdir -p $proj/{backend,frontend,deployment,data,logs}
                echo 'Initializing python environment'
                if [ ! -d $proj/.venv ];then
                    python -m venv $proj/.venv
                fi
                source $proj/.venv/bin/activate
                pip install -U pip
                if [ ! -f $proj/requirements.txt ];then
                    pip install -r $proj/requirements.txt
                fi
                deactivate
                echo -e ' Setting environment finished'
            }
            install_all() {
                system_update()
                install_software()
                install_nginx()
                install_redis()
                install_pyenv()
                set_pyenv_conf()
                install_python()
                project_init()
            }
            cat << EOF
            Type the number for the operation to execute: [1-9]
            ====================================================
            [1] system update
            [2] install system component
            [3] install Nginx
            [4] installRedis
            [5] install Pyenv
            [6] write pyenv conf
            [7] install Python
            [8] initialize project environment
            [9] all of above
            [Q] quit
            ====================================================
            EOF

            if [[ -n $1 ]]; then    # $1 first input param   $0 command   $# input count
                input=$1
                echo "execute operation: $1"
            else
                read -p "please select: " input
            fi

            case $input in
                1) system_update;;
                2) install_software;;
                3) install_nginx;;
                4) install_redis;;
                5) install_pyenv;;
                6) set_pyenv_conf;;
                7) install_python;;
                8) project_init;;
                9) install_all;;
                *) exit;;
            esac

        start.sh
            #!/bin/bash
            PROJECT="/opt/djangoSample"
            cd $PROJECT
            source $PROJECT/.venv/bin/activate
            gunicorn -c djangoSample/gunicorn-config.py djangoSample.wsgi
            deactivate
            cd -

        stop.sh
            #!/bin/bash
            PROJECT="/opt/djangoSample"
            #close gunicorn
            cat $PROJECT/logs/gunicorn.pid | xargs kill

        restart
            #!/bin/bash
            PROJECT="/opt/djangoSample"
            cat $PROJECT/logs/gunicorn.pid | xargs kill -HUP

        release.sh
            #!/bin/bash
            LOCAL_DIR="./"
            REMOTE_DIR="/opt/djangoSample"
            USER="root"
            HOST="xx.xxx.xx.xx"

            # upload code
            rsync -crvP --exclude={.git,.venv,__pycache__} $LOCAL_DIR $USER@$HOST:$REMOTE_DIR
            # start project
            ssh $USER@$HOST "$REMOTE_DIR/scripts/restart.sh"



    Fabric
        use python instead of bash write scripts

    big project structure
        proj
        |---proj/
        |   |--settings.py
        |   |--other_cofig.py
        |   |--urls.py
        |   |--wsgi.py
        |---common/
        |   |--errors.py
        |   |--keys.py
        |   |--middleware.py
        |---app1/
        |   |--migrations/
        |   |--app.py
        |   |--helper.py  / logic.py
        |   |--models.py
        |   |--views.py  (api.py)
        |---lib/
        |   |--cache.py
        |   |--http.py
        |   |--orm.py
        |   |--sms.py
        |---worker/
        |   |--__init__.py
        |   |--config.py
        |---manage.py





'''































