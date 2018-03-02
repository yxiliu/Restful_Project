from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import exceptions
from django.http import JsonResponse,HttpResponse
from rest_framework.viewsets import ModelViewSet,generics
generics.GenericAPIView
from luffy import models
from luffy import utils
from django.db import transaction
from django.db.models import F
import datetime
class Login(APIView):
    '''
    code:    1000 正确
             1010 错误
    '''
    authentication_classes = [utils.LoginAuthentication,]
    def post(self,request):
        data={'code':1000,'detail':'登录成功'}
        if not request.user:
            data['code']=1010
            data['detail'] = '登录失败，账号或密码有误！'
            return JsonResponse(data)
        data["token"]=request.auth.userauthtoken.token
        data["username"]=request.user
        return JsonResponse(data)

class News(APIView):
    def get(self,request,*args,**kwargs):
        self.dispatch
        ret={'code':1000,"detail":"News",'newslist':None}
        article_list = models.Article.objects.all()
        ser = utils.ArticleSerializer(instance=article_list, many=True, context={'request': request})
        ret['newslist']= ser.data
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
        ret={'code':1000,"detail":"NewsDetail",'detaillist':[]}
        article_obj = models.Article.objects.get(pk = nid)
        ser = utils.ArticleSerializer(instance=article_obj, context={'request': request})
        ret['detaillist'].append(ser.data)
        return JsonResponse(ret)

class ArticleCollection(APIView):
    authentication_classes = [utils.TokenAuthentication,]
    def get(self,request,nid,*args,**kwargs):
        ret = {'code': 1010, "detail": "收藏", 'data': None}
        if not request.user:
            return JsonResponse(ret)

        article_obj = models.Article.objects.get(id=nid)
        type_obj = models.ContentType.objects.get(app_label='luffy',model='article')
        collection_obj = models.Collection.objects.filter(content_type=type_obj,object_id=nid,account_id=request.user.user_id)#
        if not collection_obj:
            with transaction.atomic():
                ctime = datetime.datetime.now()
                models.Collection.objects.create(content_object=article_obj,account_id=request.user.user_id,date=ctime)
                article_obj.collect_num +=1
                article_obj.save()

                ret['code']=1000
                ret['detail']='完成收藏'
                ret['data']={'collect_num':article_obj.collect_num}
                return JsonResponse(ret)
        ret['code']=1020
        ret['detail']='已收藏'
        return JsonResponse(ret)




