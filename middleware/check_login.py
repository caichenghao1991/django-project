import logging

from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class CheckLoginMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        #print('---CheckLoginMiddleWare---', 'process request')
        msg = '%s visited %s' %(request.META.get('REMOTE_ADDR'), request.get_raw_uri())
        logging.getLogger('django').info(msg)
        #print(request.path, request.COOKIES)
        if request.path not in ('/student/login', '/') and not request.path.startswith('/admin/'):
            if not request.session.get('student') and not request.COOKIES.get('token') and not cache.has_key('student'):
                return redirect('/student/login')


    def process_view(self, request, callback, callback_args, callback_kwargs):
        # callback is calling view function
        #print('---CheckLoginMiddleWare---', 'process view')
        # callback_kwargs['page']=request.GET.get('page',1)   # view: page = kwargs.get('page',5 )
                    # modify parameter when url is not allowing add parameter, view function must have page
        #print(callback, callback_args,callback_kwargs)
        pass
    def process_response(self, request, response):
        #print('---CheckLoginMiddleWare---', 'process response')
        return response

    def process_exception(self, request, exception):
        #print('---CheckLoginMiddleWare---', 'process exception')
        print(exception)
        return HttpResponse('Something went wrong: %s' % exception)