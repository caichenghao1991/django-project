"""djangoSample URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import random

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import path, include

from mainapp.api import api_router
from mainapp.tasks import hello_celery



def index(request: HttpRequest):
    houses = [{'id': 1, 'name': "Gryffindor"}, {'id': 2, 'name': "Hufflepuff"},
              {'id': 3, 'name': "Ravenclaw"}, {'id': 4, 'name': "Slytherin"}]
    # return HttpResponse('<h1>hi, Django</h1>'.encode('utf-8'))
    lucky = houses[random.randint(1, 4) - 1]

    res = hello_celery.delay(1, 2)
    # time.sleep(2)
    # print(res.result)

    return render(request, 'index.html', {'houses': houses, 'msg': 'Hogwarts houses','lucky':lucky})
    # request, template name, context(dict)
    #return JsonResponse({'code': 201, 'msg': 'getting data'})


urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', index),
                  path('student/', include('mainapp.urls', namespace='hogwarts')),
                  path('api/', include(api_router.urls)),
                  path('api-auth/', include('rest_framework.urls'))

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
