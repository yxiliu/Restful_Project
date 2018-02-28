from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import exceptions
from django.http import JsonResponse,HttpResponse
from luffy import models
class Login(APIView):
    def post(self,request):
        data={'state':False,'code':1000,'msg':'登录失败，账号或密码有误！'}
        username = request.data.get('username')
        password = request.data.get('password')
        user_obj = models.Account.objects.filter(username=username,password=password)
        print(user_obj)
        if not user_obj:
            response = JsonResponse(data)
            response['Access-Control-Allow-Origin'] = "*"
            return response

        data['state']=True
        data['msg']='登录成功'
        data['code']=1001

        token = models.UserAuthToken.objects.get(user=user_obj).token
        data["token"]=token
        data["username"]=models.UserAuthToken.objects.get(user=user_obj).user.username

        # response.set_cookie('token',token)
        # response.set_cookie('username',username)
        response = JsonResponse(data)
        response['Access-Control-Allow-Origin'] = "*"
        return response

    def options(self, request, *args, **kwargs):
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = 'content-type'
        return response


class CoursesView(APIView):
    def get(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        if pk:
            title=models.CourseSubCategory.objects.filter(id=pk).first().name
            ret = {
                'title':title,
                # 'summary':'老师，太饿了。怎么还不下课'
            }
        else:
            course_list=[]
            course_query=models.CourseSubCategory.objects.all().values_list("id","name").order_by("id")
            for course in course_query:
                course_list.append({"id": course[0], "name": course[1]})
            ret = {'code':1000,'courseList':None}
            ret["courseList"]=course_list
        response = JsonResponse(ret)
        response['Access-Control-Allow-Origin'] = "*"
        return response