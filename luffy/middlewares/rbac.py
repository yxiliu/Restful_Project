import re

from django.shortcuts import redirect,HttpResponse
from django.http import JsonResponse
from django.conf import settings

class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response

class LoginMiddleware(MiddlewareMixin):
    # def process_request(self,request):
    #     if request.path_info == '/login/' :
    #         return None
    #     if request.COOKIES.get(settings.COOKIES_KEY,None):
    #         return None
    #     return JsonResponse({'state':False,'msg':'登录后才能访问'})

    def process_response(self,request,response):
        response['Access-Control-Allow-Origin'] = "*"
        response['Access-Control-Allow-Headers'] = 'content-type'
        response['Access-Control-Allow-Methods'] = '*'
        return response

class RbacMiddleware(MiddlewareMixin):

    def process_request(self,request):
        print(request.body)
        username = request.GET.get('cookie')
        print(username)
        if request.path=="/login/":
            return None
        if username!="null":
            return None
        else:
            print(111)
            return JsonResponse({'rbac': False})

