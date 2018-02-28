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
        # response = HttpResponse()
        # response['Access-Control-Allow-Origin'] = '*'
        # response['Access-Control-Allow-Headers'] = '*'

        return HttpResponse()

class News(APIView):
    # authentication_classes = [utils.MyAuthentication,]
    def get(self,request,*args,**kwargs):
        self.dispatch
        ret={'state':True,"msg":"News",'newslist':None}

        article_list = models.Article.objects.values('id','title','brief','head_img','date',
                               'view_num','comment_num','collect_num')
        newslist=[]
        for article in article_list:
            article['date'] = article['date'].strftime('%Y-%m-%d')
            newslist.append(article)

        ret['newslist']=newslist
        # response = JsonResponse(ret)
        # response['Access-Control-Allow-Origin'] = '*'
        return JsonResponse(ret)

    def options(self, request, *args, **kwargs):
        # response = HttpResponse()
        # response['Access-Control-Allow-Origin'] = '*'
        # response['Access-Control-Allow-Headers'] = '*'
        return HttpResponse()

class NewsDetail(APIView):
    # authentication_classes = [utils.MyAuthentication,]
    def get(self,request,nid,*args,**kwargs):

        # print(request.COOKIES)

        ret={'state':True,"msg":"NewsDetail",'detaillist':None}
        # print(request.path,nid)
        detail_list = models.Article.objects.filter(id=nid).values('title',
                           'date','view_num','agree_num','collect_num','content','source__name')
        detaillist=[]
        for item in detail_list:
            item['date'] = item['date'].strftime('%Y-%m-%d')
            detaillist.append(item)
        ret['detaillist']=detaillist
        # response = JsonResponse(ret)
        # response['Access-Control-Allow-Origin'] = '*'
        return JsonResponse(ret)

    def options(self, request, *args, **kwargs):
        # response = HttpResponse()
        # response['Access-Control-Allow-Origin'] = '*'
        # response['Access-Control-Allow-Headers'] = '*'
        return HttpResponse()
