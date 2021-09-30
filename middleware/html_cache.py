
from django.core.cache import caches
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class CachePageMiddleware(MiddlewareMixin):
    cache_page_path = {'/': {'time_out': 5, 'cache_method': 'file_cache'}}

    def process_request(self, request):

        if request.path in self.cache_page_path.keys():

            method = self.cache_page_path[request.path]['cache_method']
            print(method)
            if method and caches[method].has_key(request.path):
                print('a')
                return HttpResponse(caches[method].get(request.path))

    def process_response(self, request, response):
        if request.path in self.cache_page_path.keys():
            method = self.cache_page_path[request.path]['cache_method']
            caches[method].add(request.path, response.content, timeout=3)
        return response