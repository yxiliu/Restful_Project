from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import exceptions
from django.http import JsonResponse,HttpResponse
from luffy import models

from luffy import utils
import datetime

class Login(APIView):
    authentication_classes = []
    def post(self,request):
        data={'state':False,'code':1000,'msg':'登录失败，账号或密码有误！'}
        username = request.data.get('username')
        password = request.data.get('password')
        user_obj = models.Account.objects.filter(username=username,password=password)
        print(user_obj)
        if not user_obj:
            return JsonResponse(data)

        data['state']=True
        data['msg']='登录成功'
        data['code']=1001

        token = models.UserAuthToken.objects.get(user=user_obj).token
        data["token"]=token
        data["username"]=models.UserAuthToken.objects.get(user=user_obj).user.username

        return JsonResponse(data)

    def options(self, request, *args, **kwargs):
        return HttpResponse()

class News(APIView):
    def get(self,request,*args,**kwargs):
        self.dispatch
        ret={'state':True,"msg":"News",'newslist':None}
        article_list = models.Article.objects.values('id', 'title', 'brief', 'head_img', 'date',
                                                     'view_num', 'comment_num', 'collect_num')
        newslist = []
        for article in article_list:
            article['date'] = article['date'].strftime('%Y-%m-%d')
            newslist.append(article)

        ret['newslist'] = newslist
        return JsonResponse(ret)


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
    
    def options(self, request, *args, **kwargs):
        return HttpResponse()

class NewsDetail(APIView):
    def get(self,request,nid,*args,**kwargs):
        ret={'state':True,"msg":"NewsDetail",'detaillist':None}
        detail_list = models.Article.objects.filter(id=nid).values('title',
                           'date','view_num','agree_num','collect_num','content','source__name')
        detaillist=[]
        for item in detail_list:
            item['date'] = item['date'].strftime('%Y-%m-%d')
            detaillist.append(item)
        ret['detaillist']=detaillist
        return JsonResponse(ret)

    def options(self, request, *args, **kwargs):
        return HttpResponse()

