from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import exceptions
from django.contrib.contenttypes.models import ContentType
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
            obj=models.Course.objects.filter(id=pk).first()
            title=obj.name
            brief=obj.brief
            period=obj.period
            level=obj.get_level_display()
            price_policy=obj.price_policy.all()

            price_policy_list=[]
            for i in price_policy:
                price_policy_list.append({"周期":i.get_valid_period_display(),"价格":i.price})

            coursesection=obj.coursechapters.all()
            coursesection_list=[]
            for i in coursesection:
                coursesection_list.append(i.name)
            if not coursesection_list:
                coursesection_list="此课程还没有设置章节"
            #评论
            # recommend_courses= obj.recommend_by.all()
            # recommend_courses_list=[]
            # for i in recommend_courses:
            #     print(i,33333)
            #     recommend_courses_list.append(i.recommend_courses)
            # if not recommend_courses_list:
            #     recommend_courses_list="此课程还没有评论，快来评论吧！"

            #常见问题
            course_id=ContentType.objects.filter(app_label="luffy",model="course").first().id
            question_query=models.OftenAskedQuestion.objects.filter(content_type=course_id,object_id=obj.id,).all()
            question_list = []
            for i in question_query:
                question_list.append(i.question)
            if not question_list:
                question_list="此课程还没有常见问题"


            ret = {
                'title':title,
                'brief':brief,
                'coursesection_list':coursesection_list,
                # 'recommend_courses_list':recommend_courses_list
                'question_list':question_list,
                'period':period,
                'level':level,
                'price_policy_list':price_policy_list,
            }
        else:
            course_list=[]
            course_query=models.Course.objects.all().values_list("id","name","course_img","level").order_by("id")
            for course in course_query:
                course_list.append({"id": course[0], "name": course[1],"course_img":course[2],"level":course[3]})
            ret = {'code':1000,'courseList':None}
            ret["courseList"]=course_list
        response = JsonResponse(ret)
        response['Access-Control-Allow-Origin'] = "*"
        return response