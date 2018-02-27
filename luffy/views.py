from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import exceptions
from django.http import JsonResponse,HttpResponse
from luffy import models
import pymysql

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
        response = JsonResponse(data)
        response['Access-Control-Allow-Origin'] = "*"
        token = models.UserAuthToken.objects.get(user=user_obj).token
        response.set_cookie('token',token)
        response.set_cookie('username',username)
        return response

    def options(self, request, *args, **kwargs):
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = '*'
        return response


class CoursesView(APIView):


    def get(self,request,*args,**kwargs):
        conn = pymysql.connect(host='192.168.20.13', user='lw', password='lw123', database='luffycity', charset='utf8')
        cursor = conn.cursor()  # 拿到游标，即mysql>

        pk = kwargs.get('pk')
        if pk:
            cursor.execute('select name from luffy_coursesubcategory where id=%s' %(pk))
            ret = {
                'title':cursor.fetchone()[0],
                # 'summary':'老师，太饿了。怎么还不下课'
            }
        else:
            cursor.execute('select id,name from luffy_coursesubcategory order by id')
            course_list=[]
            for course in cursor.fetchall():
                course_list.append({"id": course[0], "name": course[1]})
            ret = {
                'code':1000,
                'courseList':None
            }
            ret["courseList"]=course_list
        response = JsonResponse(ret)
        response['Access-Control-Allow-Origin'] = "*"
        return response
